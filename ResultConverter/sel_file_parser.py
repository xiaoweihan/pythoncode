#coding=utf8
import re
import traceback
import cProfile
import array
from collections import deque
from header_info import *
from wind_speed_info import *
from controller_info import *
from channel_info import *
from frame_converter import *
from unit_converter import *
from component_converter import *
from group_data_manager import *
from var_name_converter import *
from group_name import *
class SelFileParser(object):
    '''
    this class implement parse the sel file
    '''

    drive_train_array = ['HSSbrakeTrq'.lower(), 'GenPwr'.lower(), 'GenAzim'.lower(), 'HssRate'.lower(),
                         'GenLoss'.lower(), 'GenTrq'.lower(),
                         'HssTrq'.lower(), 'LssRate'.lower(), 'LssTrq'.lower(), 'RotAzim'.lower(),
                         'RotSpeed'.lower()]

    def __init__(self,file_path):
        self._sel_file_path = file_path

        #header 信息
        self.header_info = Header_Info()

        #find sel header flag
        #self._find_desc_header_flag = False

        #self._have_factor = False

        #windspeedlist
        self.wind_speed_array = deque()

        #controllerlist
        self.controller_array = deque()

        #channellist
        self.channel_array = deque()

        #转换因子列表,使用同质的array来提高效率
        self.channel_factor_array = array.array('f')#[]

        #分组信息，冗余用来提高效率
        self.group_info = Group_data_manager()

    def get_factor(self,index):
        '''

        :param index:
        :return:
        '''
        #如果数组为空或者索引不合法
        if not self.channel_factor_array or len(self.channel_factor_array) <= index:
            return 1.0

        return self.channel_factor_array[index]


    @property
    def sel_file_path(self):
        '''

        :return:
        '''
        return self._sel_file_path

    @sel_file_path.setter
    def sel_file_path(self,file_path):
        '''

        :param file_path:
        :return:
        '''
        self._sel_file_path = file_path


    def parse_file(self):


        try:
            with open(self._sel_file_path, 'r') as f:

                line_index = 1
                # travel the file line by line
                for line_content in f:

                    if 2 == line_index:
                        self._parse_version_id(line_content)
                    elif 3 == line_index:
                        self._parse_time(line_content)
                    elif 4 == line_index:
                        self._parse_date(line_content)
                    elif 6 == line_index:
                        self._parse_result_file(line_content)
                    # elif 8 == line_index:
                    #     self._parse_sel_desc_header(line_content)
                    elif 9 == line_index:
                        self._parse_sel_desc_body(line_content)
                    elif 14 <= line_index <= 16:
                        self._parse_wind_speed_info(line_content)
                    #解析控制器及通道的信息
                    elif 17 <= line_index <= (12 + self.header_info.channels):
                        #如果是控制器信息
                        if self._filter_controller_info(line_content):
                            self._parse_controller_info(line_content)
                        #如果是通道信息
                        else:
                            self._parse_channel_info(line_content)
                    elif (14 + self.header_info.channels) < line_index <= (14 + self.header_info.channels + self.header_info.channels):
                        #如果dat格式为Binary
                        if self.header_info.file_format == 1:
                            self._parse_factor(line_content)
                    else:
                        pass
                    line_index += 1

                assert len(self.channel_factor_array) == self.header_info.channels

        except BaseException as e:
            print('exception info = {0},line_content = {1},traceback = {2}.'.format(str(e), line_content,traceback.print_exc()))

    def _parse_version_id(self,line_content):
        '''

        :param line_content:
        :return:
        '''
        #check the param is valid
        if not line_content:
            return False
        str_regex_pattern = r'Version ID[\s]*?:(.*)'

        regobj = re.compile(str_regex_pattern)

        results = regobj.search(line_content)

        if results is not None:
            self.header_info.version = results.group(1).strip()
            return True

        return False


    def _parse_time(self,line_content):
        '''

        :param line:
        :return:
        '''

        # check the param is valid
        if not line_content:
            return False

        str_regex_pattern = r'Time[\s]*?:(.*)'

        regobj = re.compile(str_regex_pattern)

        results = regobj.search(line_content)

        if results is not None:
            self.header_info.time_info = results.group(1).strip()
            return True

        return False

    def _parse_date(self,line_content):
        '''

        :param line:
        :return:
        '''

        # check the param is valid
        if not line_content:
            return False

        str_regex_pattern = r'Date[\s]*?:(.*)'

        regobj = re.compile(str_regex_pattern)

        results = regobj.search(line_content)

        if results is not None:
            self.header_info.date_info = results.group(1).strip()
            return True
        return False


    def _parse_result_file(self,line_content):
        '''

        :param line:
        :return:
        '''

        # check the param is valid
        if not line_content:
            return False

        str_regex_pattern = r'Result file[\s]*?:(.*)'

        regobj = re.compile(str_regex_pattern)

        results = regobj.search(line_content)

        if results is not None:
            self.header_info.dat_file_path = results.group(1).strip()
            return True

        return False

    def _parse_sel_desc_header(self,line_content):
        '''

        :param line:
        :return:
        '''

        # check the param is valid
        if not line_content:
            return False

        str_regex_pattern = r'[\s]+?Scans[\s]+?Channels[\s]+?Time \[sec\][\s]+?Format'

        regobj = re.compile(str_regex_pattern)

        results = regobj.match(line_content)

        #match succeed
        if results is not None:
            self._find_desc_header_flag = True
            return True
        return False


    def _parse_sel_desc_body(self,line_content):
        '''

        :param line:
        :return:
        '''

        # check the param is valid
        if not line_content:
            return False


        #remove the space
        total_content = line_content.strip()
        split_results = total_content.split()

        if split_results:
            # scans value
            self.header_info.scans = int(split_results[0])
            # channels value
            self.header_info.channels = int(split_results[1])
            # time value
            self.header_info.total_time = float(split_results[2])
            # format value
            file_format = split_results[3].strip()

            if file_format.upper() == 'ASCII':
                self.header_info.file_format = 0
            else:
                self.header_info.file_format = 1

            return True

        return False


    def _parse_wind_speed_info(self,line_content):
        '''

        :param line_content:
        :return:
        '''
        # check the param is valid
        if not line_content:
            return False
        str_regex_pattern = r'[\s]+?(\d) [\s]+?(WSP.*?) [\s]+?(\S+?) [\s]+?(.*)'
        regobj = re.compile(str_regex_pattern)
        results = regobj.match(line_content)

        if results is not None:
            # print('1 = {0},2 = {1}, 3 = {2},4 = {3}'.format(results.group(1).strip(),results.group(2).strip()
            #                                                 ,results.group(3).strip(),results.group(4).strip()))
            channel_index = int(results.group(1))
            if 2 == channel_index:
                temp_wind_speed_info = WindSpeedInfo('Wind1VelX',results.group(3).strip(),channel_index,'G','Environment')
                self.wind_speed_array.append(temp_wind_speed_info)
                # 添加分组信息
                self.group_info.add_group('Environment')
            elif 3 == channel_index:
                temp_wind_speed_info = WindSpeedInfo('Wind1VelY',results.group(3).strip(),channel_index,'G','Environment')
                self.wind_speed_array.append(temp_wind_speed_info)
                # 添加分组信息
                self.group_info.add_group('Environment')
            elif 4 == channel_index:
                temp_wind_speed_info = WindSpeedInfo('Wind1VelZ',results.group(3).strip(),channel_index,'G','Environment')
                self.wind_speed_array.append(temp_wind_speed_info)
                # 添加分组信息
                self.group_info.add_group('Environment')
            else:
                pass
            return True
        return False


    def _parse_controller_info(self,line_content):
        '''

        :param line_content:
        :return:
        '''
        # check the param is valid
        if not line_content:
            return False

        #reg_pattern = r'.+:\s*?(\d+)(.*?)-\s*?units:\((\w+?)\)$'
        #reg_pattern = r'\s+?(\d+)\s+?DLL.*DLL.*:\s+?\d+(.*?)-\s*?units:\((\w+?)\)\s*?'
        reg_pattern = r'\s+?(\d+)\s+?DLL.*__(.+?)-\s*?units:\((.+?)\)\s+?'
        obj = re.compile(reg_pattern)
        results = obj.match(line_content)

        if results:
            channel_index = int(results.group(1))
            controller_name = results.group(2).strip()
            #进行单位转换
            controller_unit = Unit_Converter.convert_unit(results.group(3).strip())

            #进行分组
            lower_controller_name = controller_name.lower()
            # 判断是否drive train
            if lower_controller_name in SelFileParser.drive_train_array:
                self.group_info.add_group('Drive train')
                temp_controller_info = Controller_Info(controller_name, controller_unit, channel_index,None,'Drive train')
                self.controller_array.append(temp_controller_info)
            else:
                self.group_info.add_group('Others')
                temp_controller_info = Controller_Info(controller_name, controller_unit, channel_index,None,'Others')
                self.controller_array.append(temp_controller_info)

            return True

        # else:
        #     reg_pattern = r'\s+?(\d+)\s+?DLL.*DLL.*:\s+?\d+(.*)\s*?'
        #     obj = re.compile(reg_pattern)
        #     results = obj.match(line_content)
        #     if results:
        #         channel_index = int(results.group(1))
        #         controller_name = results.group(2).strip()
        #         # 进行单位转换
        #         controller_unit = '-'
        #         temp_controller_info = Controller_Info(controller_name, controller_unit,channel_index)
        #         self.controller_array.append(temp_controller_info)
        #         return True

        return False

    def _filter_controller_info(self,line_content):
        '''

        :param line_content:
        :return:
        '''
        if not line_content:
            return False

        str_regex_pattern = r'^[\s]+?(\d+?)[\s]+DLL.*\s+?'
        regobj = re.compile(str_regex_pattern)
        results = regobj.match(line_content)

        if results:
            return True
        return False

    def _parse_channel_info(self, line_content):
        '''

        :param self:
        :param line_content:
        :return:
        '''
        if not line_content:
            return False

        #对每行数据进行正则过滤
        #reg_pattern = r'\s+?(\d+)\s+?([FM][xyz])\s*?coo:\s*?(\w+)\s+?(\w+).*__(\w+)_(\w+)\s+?'
        #reg_pattern = r'\s+?(\d+)\s+?([FM][xyz])\s*?coo:\s*?(\w+)\s+?(\w+).*__([a-zA-Z0-9]+)(.*)\s+?'
        reg_pattern = r'\s+?(\d+)\s+?([\w\s]+)\s*?coo:\s*?(\w+)\s+?(\w+).*__([A-Za-z0-9]+)(.*)\s+?'
        obj = re.compile(reg_pattern)
        #查看是否符合
        results = obj.match(line_content)
        #如果符合
        if results:
            #print('var_name = {0},frame_name = {1},var_unit = {2},componet_name = {3},section_name = {4}'.format(results.group(1).strip(), results.group(2).strip(), results.group(3).strip(),
            #      results.group(4).strip(), results.group(5).strip()))

            #channel_index
            channel_index = int(results.group(1).strip())
            #var_name
            var_name = Var_Name_Converter.convert_var_name(results.group(2).strip())
            #frame_name
            frame_name = Frame_Converter.convert_frame(results.group(3).strip())
            #var_unit
            var_unit = Unit_Converter.convert_unit(results.group(4).strip())
            #section_name
            #有的部件没有section有的部件存在section，所以这个地方需要分开
            section_name = results.group(6).strip()

            if section_name:
                if section_name[0] == '_' and section_name[1] == 'z':
                    section_name = section_name[1:].upper()
                    # component_name
                    component_name = Component_Converter.convert_Component(results.group(5).strip())
                #处理yaw
                else:
                    # component_name
                    component_name = Component_Converter.convert_Component(results.group(5).strip() + section_name)
                    section_name = None
            else:
                component_name = Component_Converter.convert_Component(results.group(5).strip())


            #进行分组
            if component_name.startswith('B') and frame_name.startswith('H'):
                self.group_info.add_group('Hub')
                temp_channel_info = Channel_Info(var_name, component_name, frame_name, var_unit, section_name,
                                                 channel_index,'Hub')
                self.channel_array.append(temp_channel_info)
            else:
                group_name = Group_Name.convert_group_name(component_name)
                self.group_info.add_group(group_name)
                temp_channel_info = Channel_Info(var_name, component_name, frame_name, var_unit, section_name,
                                                 channel_index,group_name)
                self.channel_array.append(temp_channel_info)


            return True
        return False

    def _parse_factor(self,line_content):
        '''

        :param line_content:
        :return:
        '''
        if not line_content:
            return False

        factor = float(line_content.strip())
        self.channel_factor_array.append(factor)

        return True


def main():

    sel_file_path = r'D:\test_dat\en121_alf_test_final_b.sel'
    Parser = SelFileParser(sel_file_path)
    Parser.parse_file()





    print(Parser.header_info)


    print('wind_speed_array size = {0}'.format(len(Parser.wind_speed_array)))
    for element in Parser.wind_speed_array:
        print(element)

    print('*******************************************************')
    print('controller_array size = {0}'.format(len(Parser.controller_array)))
    for element in Parser.controller_array:
        print(element)

    print('########################################################')
    print('channel_array size = {0}'.format(len(Parser.channel_array)))
    for element in Parser.channel_array:
        print(element)

    print(Parser.channel_factor_array)
    print(len(Parser.channel_factor_array))


if __name__ == '__main__':
    main()