#coding=utf8

import os
import time
import h5py
import collections
import socket
# import multiprocessing
# import concurrent.futures
from datetime import *
from Connector import ttypes
from Connector import ResultConverter

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


from sel_file_parser import *
from dat_file_parser import *
from log import loggerInstance
from utility import *
from unit_normalize import *
from coordinate_converter import *

class ConcreteResultConverter(object):

    '''

    '''

    MAX_VALUE = 1E26
    MIN_VALUE = -1E26

    def _valid_data(self,data_array):
        '''

        :param data_array:
        :return:
        '''

        result = np.ptp(data_array)


        if result < (self.MAX_VALUE - self.MIN_VALUE):
            return True

        return False


    def inner_convert_result_split_block(self,element):
        '''
        this is write tdc split more blocks
        :param element:
        :return:
        '''

        loggerInstance.debug_log('convert request comes...')
        delete_h5_flag = False
        try:

            begin_time = datetime.now()#time.time()

            if not element:
                loggerInstance.error_log('the param is invalid.')
                return False
            # 获取转换的信息
            # HAWc2结果文件所在目录
            strResultDir = element.strResultDir
            # 生成h5之后需要拷贝的目录
            strCopyDir = element.strCopyDir
            strHtcFilePath = element.strHtcFilePath
            costTime = element.costTime
            loggerInstance.debug_log(
                'ResultDir = {0},CopyDir = {1},HtcFilePath = {2},CostTime = {3}.'.format(strResultDir, strCopyDir,
                                                                                         strHtcFilePath, costTime))

            # 判断htcfile是否存在
            if not os.path.exists(strHtcFilePath):
                loggerInstance.error_log('the {0} is not exist.'.format(strHtcFilePath))
                return False

            # 判断结果文件目录是否是一个目录
            if not os.path.isdir(strResultDir):
                loggerInstance.error_log('the {0} is not dir.'.format(strResultDir))
                return False

            # 判断拷贝文件目录是否是一个目录
            if not os.path.isdir(strCopyDir):
                loggerInstance.error_log('the {0} is not dir.'.format(strCopyDir))
                return False

            # 遍历resultdir文件夹，找出后缀名为sel与dat的
            for file_name in travel_dir(strResultDir):

                if file_name.endswith('.sel'):
                    str_sel_file_name = file_name

                elif file_name.endswith('.dat'):
                    str_dat_file_name = file_name

                else:
                    pass

            # 判断文件是否存在
            if not str_sel_file_name or not str_dat_file_name:
                loggerInstance.error_log(
                    'the sel_path = {0},the dat_path ={1}'.format(str_sel_file_name, str_dat_file_name))
                return False

            # 开始解析sel文件
            sel_parser = SelFileParser(str_sel_file_name)
            sel_parser.parse_file()

            # 开始解析dat文件如果dat文件为二进制格式
            if sel_parser.header_info.file_format == 1:
                dat_parser = BinaryDatFileParser(str_dat_file_name, sel_parser.header_info.scans,
                                                 sel_parser.header_info.channels)
            # 为文本格式
            else:
                dat_parser = AsciiDatFileParser(str_dat_file_name, sel_parser.header_info.scans,
                                                sel_parser.header_info.channels)

            # 数据文件
            data_array = dat_parser.parse_dat_file()

            if data_array is None:
                loggerInstance.error_log('parse dat file {0} failed.'.format(str_dat_file_name))
                return False

            # 组装h5文件
            sel_file_name, sel_file_extension = os.path.splitext(os.path.basename(str_sel_file_name))
            str_h5_file_path = os.path.join(strResultDir, sel_file_name)
            str_h5_file_path += '.h5'

            # 创建h5文件
            h5_root = h5py.File(str_h5_file_path, 'w')

            # 创建group
            h5_file_group = h5_root  # h5_root.create_group(os.path.basename(str_h5_file_path))

            # 创建Model group
            model_group = h5_file_group.create_group('Model')
            # 设置Model的属性
            model_group.attrs['Primary_HAWC2_input_file'] = os.path.basename(strHtcFilePath)
            model_group.attrs['HAWC2_output_file'] = os.path.basename(str_h5_file_path)
            model_group.attrs['ModelDesc'] = sel_parser.header_info.version

            # 计算需要的Channels
            nActualChannels = len(sel_parser.wind_speed_array) + len(sel_parser.controller_array) + len(
                sel_parser.channel_array)

            # 创建SimResults group
            sim_results_group = h5_file_group.create_group('SimResults')

            # 生成channelnames
            channel_name_data_set = sim_results_group.create_dataset('ChanNames', (nActualChannels,), dtype='S20')

            #生成ChanNamesIndex
            channel_name_index_data_set = sim_results_group.create_dataset('ChanNamesIndex', (nActualChannels,), dtype=np.int32)

            # 生成Chanunit
            channel_unit_data_set = sim_results_group.create_dataset('ChanUnits', (nActualChannels,), dtype='S9')

            time_data = data_array[:, 0] * sel_parser.get_factor(0)

            #创建分块的TDC
            block_tdc_name_dict = {}

            for k,v in sel_parser.group_info.group_dict.items():
                block_tdc_name_dict[k] = sim_results_group.create_dataset(k,(v.group_num,sel_parser.header_info.scans),dtype=np.float32)

            # 验证数据合法性
            if not self._valid_data(time_data):
                loggerInstance.error_log('the data is out of range!')
                delete_h5_flag = True
                return False
            sim_results_group.create_dataset('Time', data=time_data)
            # 生成Simulation
            simulation_group = h5_file_group.create_group('Simulation')

            # 生成Statistics
            statistics_group = h5_file_group.create_group('Statistics')

            # 生成ChanMaxTStep dataset
            chan_max_step_data_set = statistics_group.create_dataset('ChanMaxTStep', (nActualChannels,), dtype=np.int32)

            # 生成ChanMean dataset
            chan_max_value_data_set = statistics_group.create_dataset('ChanMaxVal', (nActualChannels,),
                                                                      dtype=np.float32)

            # 生成ChanMean dataset
            chan_mean_value_data_set = statistics_group.create_dataset('ChanMean', (nActualChannels,), dtype=np.float32)

            # 生成ChanMinTStep dataset
            chan_min_step_data_set = statistics_group.create_dataset('ChanMinTStep', (nActualChannels,), dtype=np.int32)

            # 生成ChanMinval dataset
            chan_min_value_data_set = statistics_group.create_dataset('ChanMinVal', (nActualChannels,),
                                                                      dtype=np.float32)

            # 生成ChanstDev dataset
            chan_stdev_data_set = statistics_group.create_dataset('ChanStDev', (nActualChannels,), dtype=np.float32)

            current_index = 0
            # 转换风速的信息
            for element in sel_parser.wind_speed_array:
                # 进行单位转换
                channel_unit, factor = Unit_Normalizer.normalize_unit(element.wind_speed_unit)
                # 进行坐标系转换
                channel_transfor_factor, channel_name = Coordinate_Converter.convert_coordinate(element.frame_name,
                                                                                                element.wind_speed_name)
                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1) * channel_transfor_factor

                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                # 写入channelname信息
                channel_name_data_set[current_index] = np.string_(channel_name)
                # 写入channelunit信息
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                # 写入数据信息
                block_tdc_name_dict[element.group_name][sel_parser.group_info.get_group_write_pos(element.group_name),:] = channel_data
                #记录索引
                channel_name_index_data_set[current_index] = sel_parser.group_info.get_group_write_pos(element.group_name)
                sel_parser.group_info.write_group(element.group_name)

                # 写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                # 写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                # 写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                # 写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                # 写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                # 写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1

            # 转换控制器的信息
            for element in sel_parser.controller_array:
                # 进行单位转换
                channel_unit, factor = Unit_Normalizer.normalize_unit(element.controller_unit)
                # 控制器不需要坐标系转换
                channel_name = element.controller_name
                # channel_transfor_factor,channel_name = Coordinate_Converter.convert_coordinate(element.frame_name,element.controller_name)
                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1)

                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                # 写入channelname信息
                channel_name_data_set[current_index] = np.string_(channel_name)
                # 写入channelunit信息
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                # 写入数据信息
                block_tdc_name_dict[element.group_name][sel_parser.group_info.get_group_write_pos(element.group_name),:] = channel_data
                #记录索引
                channel_name_index_data_set[current_index] = sel_parser.group_info.get_group_write_pos(element.group_name)
                sel_parser.group_info.write_group(element.group_name)
                # 写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                # 写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                # 写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                # 写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                # 写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                # 写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1

            # 转换通道的信息
            for element in sel_parser.channel_array:
                # 单位归一化
                channel_unit, factor = Unit_Normalizer.normalize_unit(element.var_unit)

                # 进行坐标系转换
                channel_transfor_factor, channel_var_name = Coordinate_Converter.convert_coordinate(element.frame_name,
                                                                                                    element.var_name)

                # 如果存在section
                if element.section_name:
                    channel_name = element.component_name + '_' + element.section_name + '_' + channel_var_name + element.frame_name
                else:
                    channel_name = element.component_name + '_' + channel_var_name + element.frame_name

                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1) * channel_transfor_factor

                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                channel_name_data_set[current_index] = np.string_(channel_name)
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                # 写入数据信息
                block_tdc_name_dict[element.group_name][sel_parser.group_info.get_group_write_pos(element.group_name),:] = channel_data
                #记录索引
                channel_name_index_data_set[current_index] = sel_parser.group_info.get_group_write_pos(element.group_name)
                sel_parser.group_info.write_group(element.group_name)
                # 写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                # 写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                # 写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                # 写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                # 写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                # 写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1
            end_time = datetime.now()
            loggerInstance.debug_log('cost time = {0} seconds.'.format((end_time - begin_time).seconds))
            return True
        except BaseException as e:
            loggerInstance.fatal_log('this is something wrong {0}.', e)
            return False
        finally:
            h5_root.flush()
            h5_root.close()

            # 如果需要删除h5文件
            if delete_h5_flag:
                os.remove(str_h5_file_path)
            loggerInstance.debug_log('convert request go...')





    def inner_convert_result(self, element):
        '''

        :param element:
        :return:
        '''

        loggerInstance.debug_log('convert request comes...')
        delete_h5_flag = False
        try:

            begin_time = datetime.now()

            if not element:
                loggerInstance.error_log('the param is invalid.')
                return False
            #获取转换的信息
            #HAWc2结果文件所在目录
            strResultDir = element.strResultDir
            #生成h5之后需要拷贝的目录
            strCopyDir = element.strCopyDir
            strHtcFilePath = element.strHtcFilePath
            costTime = element.costTime
            loggerInstance.debug_log('ResultDir = {0},CopyDir = {1},HtcFilePath = {2},CostTime = {3}.'.format(strResultDir,strCopyDir,
                                     strHtcFilePath,costTime))

            #判断htcfile是否存在
            if not os.path.exists(strHtcFilePath):
                loggerInstance.error_log('the {0} is not exist.'.format(strHtcFilePath))
                return False

            #判断结果文件目录是否是一个目录
            if not os.path.isdir(strResultDir):
                loggerInstance.error_log('the {0} is not dir.'.format(strResultDir))
                return False

            # 判断拷贝文件目录是否是一个目录
            if not os.path.isdir(strCopyDir):
                loggerInstance.error_log('the {0} is not dir.'.format(strCopyDir))
                return False


            #遍历resultdir文件夹，找出后缀名为sel与dat的
            for file_name in travel_dir(strResultDir):

                if file_name.endswith('.sel'):
                    str_sel_file_name = file_name

                elif file_name.endswith('.dat'):
                    str_dat_file_name = file_name

                else:
                    pass


            #判断文件是否存在
            if not str_sel_file_name or not str_dat_file_name:
                loggerInstance.error_log('the sel_path = {0},the dat_path ={1}'.format(str_sel_file_name,str_dat_file_name))
                return False

            #开始解析sel文件
            sel_parser = SelFileParser(str_sel_file_name)
            sel_parser.parse_file()


            #开始解析dat文件如果dat文件为二进制格式
            if sel_parser.header_info.file_format == 1:
                dat_parser = BinaryDatFileParser(str_dat_file_name,sel_parser.header_info.scans,sel_parser.header_info.channels)
            #为文本格式
            else:
                dat_parser = AsciiDatFileParser(str_dat_file_name,sel_parser.header_info.scans,sel_parser.header_info.channels)

            #数据文件
            data_array = dat_parser.parse_dat_file()

            if data_array is None:
                loggerInstance.error_log('parse dat file {0} failed.'.format(str_dat_file_name))
                return False



            #组装h5文件
            sel_file_name,sel_file_extension = os.path.splitext(os.path.basename(str_sel_file_name))
            str_h5_file_path = os.path.join(strResultDir,sel_file_name)
            str_h5_file_path += '.h5'

            #创建h5文件
            h5_root = h5py.File(str_h5_file_path,'w')

            #创建group
            h5_file_group = h5_root#h5_root.create_group(os.path.basename(str_h5_file_path))

            #创建Model group
            model_group = h5_file_group.create_group('Model')
            #设置Model的属性
            model_group.attrs['Primary_HAWC2_input_file'] = os.path.basename(strHtcFilePath)
            model_group.attrs['HAWC2_output_file'] = os.path.basename(str_h5_file_path)
            model_group.attrs['ModelDesc'] = sel_parser.header_info.version

            #计算需要的Channels
            nActualChannels = len(sel_parser.wind_speed_array) + len(sel_parser.controller_array) + len(sel_parser.channel_array)

            #创建SimResults group
            sim_results_group = h5_file_group.create_group('SimResults')


            #生成channelnames
            channel_name_data_set = sim_results_group.create_dataset('ChanNames',(nActualChannels,),dtype='S20')

            #生成Chanunit
            channel_unit_data_set = sim_results_group.create_dataset('ChanUnits', (nActualChannels,),dtype='S9')

            #生成TDC dataset
            #tdc_data_set = sim_results_group.create_dataset('TDC', (sel_parser.header_info.scans,nActualChannels),dtype=np.float32)
            tdc_data_set = sim_results_group.create_dataset('TDC', (nActualChannels,sel_parser.header_info.scans),dtype=np.float32)

            #time_data = data_array[:,0] * sel_parser.get_factor(0)
            time_data = data_array[0,:] * sel_parser.get_factor(0)
            #验证数据合法性
            if not self._valid_data(time_data):
                loggerInstance.error_log('the data is out of range!')
                delete_h5_flag = True
                return False
            sim_results_group.create_dataset('Time',data=time_data)
            #生成Simulation
            simulation_group = h5_file_group.create_group('Simulation')

            #生成Statistics
            statistics_group = h5_file_group.create_group('Statistics')

            #生成ChanMaxTStep dataset
            chan_max_step_data_set = statistics_group.create_dataset('ChanMaxTStep',(nActualChannels,),dtype=np.int32)

            #生成ChanMean dataset
            chan_max_value_data_set = statistics_group.create_dataset('ChanMaxVal', (nActualChannels,), dtype=np.float32)

            #生成ChanMean dataset
            chan_mean_value_data_set = statistics_group.create_dataset('ChanMean', (nActualChannels,), dtype=np.float32)

            #生成ChanMinTStep dataset
            chan_min_step_data_set = statistics_group.create_dataset('ChanMinTStep', (nActualChannels,), dtype=np.int32)

            #生成ChanMinval dataset
            chan_min_value_data_set = statistics_group.create_dataset('ChanMinVal', (nActualChannels,), dtype=np.float32)

            #生成ChanstDev dataset
            chan_stdev_data_set = statistics_group.create_dataset('ChanStDev', (nActualChannels,), dtype=np.float32)

            current_index = 0
            #转换风速的信息
            for element in sel_parser.wind_speed_array:
                #进行单位转换
                channel_unit, factor = Unit_Normalizer.normalize_unit(element.wind_speed_unit)
                #进行坐标系转换
                channel_transfor_factor,channel_name = Coordinate_Converter.convert_coordinate(element.frame_name,element.wind_speed_name)
                #channel_data = data_array[:,element.channel_index - 1] * factor * sel_parser.get_factor(element.channel_index - 1) * channel_transfor_factor
                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1) * channel_transfor_factor

                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                #写入channelname信息
                channel_name_data_set[current_index] = np.string_(channel_name)
                #写入channelunit信息
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                #写入数据信息
                #tdc_data_set[:,current_index] = channel_data
                tdc_data_set[current_index,:] = channel_data
                #写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                #写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                #写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                #写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                #写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                #写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1

            #转换控制器的信息
            for element in sel_parser.controller_array:
                #进行单位转换
                channel_unit, factor = Unit_Normalizer.normalize_unit(element.controller_unit)
                #控制器不需要坐标系转换
                channel_name = element.controller_name
                #channel_transfor_factor,channel_name = Coordinate_Converter.convert_coordinate(element.frame_name,element.controller_name)
                #channel_data = data_array[:,element.channel_index - 1] * factor * sel_parser.get_factor(element.channel_index - 1)
                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1)
                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                #写入channelname信息
                channel_name_data_set[current_index] = np.string_(channel_name)
                #写入channelunit信息
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                #写入数据信息
                #tdc_data_set[:,current_index] = channel_data
                tdc_data_set[current_index,:] = channel_data
                #写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                #写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                #写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                #写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                #写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                #写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1

            #转换通道的信息
            for element in sel_parser.channel_array:
                #单位归一化
                channel_unit,factor = Unit_Normalizer.normalize_unit(element.var_unit)

                #进行坐标系转换
                channel_transfor_factor,channel_var_name = Coordinate_Converter.convert_coordinate(element.frame_name,element.var_name)

                #如果存在section
                if element.section_name:
                    channel_name = element.component_name + '_' + element.section_name + '_' + channel_var_name + element.frame_name
                else:
                    channel_name = element.component_name + '_' + channel_var_name + element.frame_name

                #channel_data = data_array[:,element.channel_index - 1] * factor * sel_parser.get_factor(element.channel_index - 1) * channel_transfor_factor
                channel_data = data_array[element.channel_index - 1,:] * factor * sel_parser.get_factor(
                    element.channel_index - 1) * channel_transfor_factor
                if not self._valid_data(channel_data):
                    loggerInstance.error_log('the data is out of range!')
                    delete_h5_flag = True
                    return False

                channel_name_data_set[current_index] = np.string_(channel_name)
                channel_unit_data_set[current_index] = np.string_(channel_unit)
                #写入数据信息
                #tdc_data_set[:,current_index] = channel_data
                tdc_data_set[current_index,:] = channel_data
                #写入最大值的索引
                chan_max_step_data_set[current_index] = np.argmax(channel_data)
                #写入最大值
                chan_max_value_data_set[current_index] = np.max(channel_data)
                #写入平均值
                chan_mean_value_data_set[current_index] = np.mean(channel_data)
                #写入最小值的索引
                chan_min_step_data_set[current_index] = np.argmin(channel_data)
                #写入最小值
                chan_min_value_data_set[current_index] = np.min(channel_data)
                #写入标准差
                chan_stdev_data_set[current_index] = np.std(channel_data)

                current_index += 1
            end_time = datetime.now()
            loggerInstance.debug_log('cost time = {0} seconds.'.format((end_time - begin_time).seconds))
            return True
        except BaseException as e:
            loggerInstance.fatal_log('this is something wrong {0}.', e)
            return False
        finally:
            h5_root.flush()
            h5_root.close()

            #如果需要删除h5文件
            if delete_h5_flag:
                os.remove(str_h5_file_path)
            loggerInstance.debug_log('convert request go...')




    def ConvertResult(self, element):
        '''

        :param element:
        :return:
        '''

        #return self.inner_convert_result_split_block(element)
        return self.inner_convert_result(element)


def main():
    try:
        handler = ConcreteResultConverter()
        processor = ResultConverter.Processor(handler)
        #transport = TSocket.TServerSocket(host=socket.gethostbyname(socket.gethostname()),port=10035)
        transport = TSocket.TServerSocket(host='127.0.0.1', port=10045)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
        # You could do one of these for a multithreaded server
        # server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
        # server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

        loggerInstance.debug_log('Starting the server...')
        server.serve()
        loggerInstance.debug_log('Bye!')

    except BaseException as e:
        loggerInstance.error_log('this is something wrong {0}',e)

if __name__ == '__main__':

    #开启服务
    main()











