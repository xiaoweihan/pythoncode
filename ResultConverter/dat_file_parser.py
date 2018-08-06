#coding=utf8
import os.path
import struct
import numpy as np
import traceback
from channel_coordinate_convert_info import *

class DatFileParser(object):

    '''

    '''
    def __init__(self,dat_file_path,scan_num,channel_num):
        self._dat_file_path = dat_file_path
        #时序值
        self._scan_num = scan_num
        #变量名
        self._channel_num = channel_num
        #self._convert_map = {}



    # def set_convert_info(self,convert_info_array):
    #     for element in convert_info_array:
    #         self._convert_map[element.channel_index] = element


    def parse_dat_file(self):
        pass

    def _is_file_exist(self):
        '''

        :return:
        '''

        #判断文件是否存在
        if not os.path.exists(self._dat_file_path):
            return False
        return True



class AsciiDatFileParser(DatFileParser):

    '''

    '''

    def parse_dat_file(self):

        try:
            # 如果dat文件不存在,则返回None
            if not super(AsciiDatFileParser, self)._is_file_exist():
                return None


            # define a matrix
            channel_data_matrix = np.zeros((self._scan_num, self._channel_num), dtype=np.double)

            with open(self._dat_file_path, 'r') as f:
                line_index = 0
                # 逐行读取
                for line_content in f:
                    # 如果长度为0，则跳过
                    if len(line_content) != 0:
                        # 对每行数据进行分割
                        channel_data_array = line_content.strip().split()
                        # 分割后的个数是否和scan相等
                        if len(channel_data_array) == self._channel_num:
                            channel_data_matrix[line_index] = channel_data_array

                    line_index += 1

            return channel_data_matrix
        except BaseException as e:
            print('exception info = {0},traceback = {1}.'.format(str(e),traceback.print_exc()))
            return None


class BinaryDatFileParser(DatFileParser):
    '''

    '''

    def __init__(self,dat_file_path,scan_num,channel_num,element_size = 2):

        super(BinaryDatFileParser,self).__init__(dat_file_path,scan_num,channel_num)
        self._element_size = element_size


    def parse_dat_file(self):

        try:
            # 如果dat文件不存在,则返回None
            if not super(BinaryDatFileParser, self)._is_file_exist():
                return None

            # 判断文件的大小是否符合规定
            file_size = os.path.getsize(self._dat_file_path)

            calc_file_size = self._element_size * self._scan_num * self._channel_num

            # 小于计算的文件大小
            if file_size < calc_file_size:
                return None

            # define a matrix
            #channel_data_matrix = np.zeros((self._channel_num, self._scan_num), dtype=np.short)
            channel_data_matrix = np.zeros((self._scan_num,self._channel_num), dtype=np.short)

            # 解析的格式化字符
            parserfmt = '@{0}h'.format(self._scan_num)

            with open(self._dat_file_path, 'rb') as f:
                # 遍历读取数据
                for x in range(self._channel_num):
                    channel_data_array = struct.unpack(parserfmt, f.read(self._element_size * self._scan_num))

                    if len(channel_data_array) == self._scan_num:
                        channel_data_matrix[:,x] = channel_data_array

            return channel_data_matrix

        except BaseException as e:
            print('exception info = {0},traceback = {1}.'.format(str(e), traceback.print_exc()))
            return None

if __name__ == '__main__':


    Parser = BinaryDatFileParser(r'd:\en121_alf_test_final_b.dat',250,1636)


    result = Parser.parse_dat_file()
    print(result)

    print(result.dtype)
    print(result.shape)


