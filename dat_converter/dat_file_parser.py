#coding=utf8
'''
parse the dat file
'''

import re
import struct
import json
import os



class DataElement(object):
    '''

    '''
    def __init__(self):
        self.data_format = -1
        self.data_bits = 0
        self.data_offset = 0
        self.data_total_length = 0
        self.use_transform = False
        self.factor = 0.0
        self.constant_factor = 0.0
        self.data_array = []
        self.var_name = None
        self.var_unit = None
        self.sample_period = 0.0

        self.custom_factor = 1.0

    def __str__(self):

        str_result_array = [str(self.data_format),str(self.data_bits),str(self.data_offset),str(self.data_total_length),str(self.use_transform),\
                     str(self.factor),str(self.constant_factor),self.var_name,str(self.sample_period),str(len(self.data_array))]

        return '    '.join(str_result_array)







class DatFileParser(object):
    '''
    this class is used to parse the dat file,read var name and values from dat files.


    '''
    def __init__(self,dat_file_path = None):
        '''

        :param dat_file_path:
        '''
        self._dat_file_path = dat_file_path
        self._dat_body_content = None
        self._head_element_array = []
        self._convert_table = None

    def get_element_info(self):
        for element in self._head_element_array:
            yield element

    @property
    def dat_file_path(self):
        '''

        :return:
        '''
        return self._dat_file_path

    @dat_file_path.setter
    def dat_file_path(self,dat_file_path):
        '''

        :param dat_file_path:
        :return:
        '''
        #
        self._dat_file_path = dat_file_path


    def _get_header_info(self):
        '''

        :return: header str

        '''

        header_info = None

        dat_content = None

        #select the header info
        with open(self._dat_file_path,'rb') as fReader:

            #get the content
            dat_content = fReader.read()

        #根据正则表达式找出header
        str_find_header_re_pattern = r'\|CS,\d,.*\d+,.*\d+,'
        match_results = re.search(str_find_header_re_pattern,dat_content)

        if match_results is not None:
            start,end = match_results.span(0)
            header_info = dat_content[:end]
            self._dat_content = bytearray(dat_content)

        return header_info

    def _select_all_result(self,str_pattern,str_content,result_array):
        '''

        :param str_pattern:
        :param str_content:
        :param result_array:
        :return:
        '''

        for element in re.finditer(str_pattern,str_content):
            result_array.append(element.group())

    def _parse_cb_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        result = content.split(',')
        if len(result) >= 15:
            data_element.data_offset = int(result[7].strip())
            data_element.data_total_length = int(result[10].strip())
            return True
        return False

    def _parse_cd_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        result = content.split(',')
        if len(result) >= 7:
            data_element.sample_period = float(result[3].strip())
            return True
        return False

    def _parse_nt_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        return True

    def _parse_cp_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        result = content.split(',')
        if len(result) >= 7:
            data_element.data_format = int(result[5].strip())
            data_element.data_bits = int(result[6].strip())
            return True
        return False

    def _parse_cr_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        result = content.split(',')
        if len(result) >= 9:

            if int(result[3].strip()) != 0:
                data_element.use_transform = True
            else:
                data_element.use_transform = False

            data_element.factor = float(result[4].strip())
            data_element.constant_factor = float(result[5].strip())
            data_element.var_unit = result[8].strip(';')
            return True
        return False

    def _parse_cn_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        result = content.split(',')
        if len(result) >= 8:
            var_name = result[7].strip()
            if var_name in self._convert_table:
                data_element.var_name = self._convert_table[var_name]['new_name']
                data_element.custom_factor = self._convert_table[var_name]['factor']
                return True
        return False


    def _parse_cg_content(self,data_element,content):
        '''

        :param data_element:
        :param content:
        :return:
        '''
        return True

    def _parse_header_info(self,header_content):
        '''

        :param header_content:
        :return:
        '''
        #解析Cb消息头
        cb_result_array = []
        str_cb_pattern = r'\|Cb,.*?;'
        self._select_all_result(str_cb_pattern,header_content,cb_result_array)

        # 解析CD消息头
        cd_result_array = []
        str_cd_pattern = r'\|CD,.*?;'
        self._select_all_result(str_cd_pattern, header_content, cd_result_array)

        # 解析NT消息头
        nt_result_array = []
        str_nt_pattern = r'\|NT,.*?;'
        self._select_all_result(str_nt_pattern, header_content, nt_result_array)

        # 解析CP消息头
        cp_result_array = []
        str_cp_pattern = r'\|CP,.*?;'
        self._select_all_result(str_cp_pattern, header_content, cp_result_array)

        # 解析CR消息头
        cr_result_array = []
        str_cr_pattern = r'\|CR,.*?;'
        self._select_all_result(str_cr_pattern, header_content,cr_result_array)

        # 解析CN消息头
        cn_result_array = []
        str_cn_pattern = r'\|CN,.*?;'
        self._select_all_result(str_cn_pattern, header_content, cn_result_array)

        # 解析CG消息头
        cg_result_array = []
        str_cg_pattern = r'\|CG,.*?;'
        self._select_all_result(str_cg_pattern, header_content, cg_result_array)

        min_array_size = min(len(cb_result_array),len(cd_result_array),len(nt_result_array),
                             len(cp_result_array),len(cr_result_array),len(cn_result_array),
                             len(cg_result_array))

        for i in xrange(min_array_size):
            data_element = DataElement()
            if (self._parse_cb_content(data_element,cb_result_array[i]) and self._parse_cd_content(data_element,cd_result_array[i]) and
                self._parse_nt_content(data_element,nt_result_array[i]) and self._parse_cp_content(data_element,cp_result_array[i]) and
                self._parse_cr_content(data_element,cr_result_array[i]) and self._parse_cn_content(data_element,cn_result_array[i]) and
                self._parse_cg_content(data_element,cg_result_array[i])):

                self._head_element_array.append(data_element)

    def _parse_body(self):
        date_format_table = ['I', 'i', 'H','h', 'L', 'l', 'f', 'd', '*', 'h', 'l']
        for element in self._head_element_array:
            #数据的偏移长度
            start_pos = 0
            data_value = None
            #每个数据占据的字节数
            data_byte = element.data_bits / 8
            while start_pos < element.data_total_length:

                if 9 == element.data_format:
                    pass
                else:
                    data_value, = struct.unpack(date_format_table[element.data_format - 1], self._dat_content[element.data_offset + start_pos:element.data_offset + start_pos + data_byte])
                    if element.use_transform:
                        data_value = element.factor * data_value + element.constant_factor
                    element.data_array.append(data_value * element.custom_factor)
                start_pos += data_byte
            #print element

    def parse_dat_file(self):
        '''
        parse the dat file
        :return:
        '''

        #加载变量名映射表
        json_path = os.getcwd() + r'\convert_table.json'

        with open(json_path,'r') as json_reader:
            self._convert_table = json.load(json_reader)

        #获取headerinfo
        header_content = self._get_header_info()
        #解析头
        self._parse_header_info(header_content)
        #解析体
        self._parse_body()













