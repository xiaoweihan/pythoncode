#coding=utf8

'''
load the mat file and convert it's data to txt file
'''
import os
import json
import scipy.io
import h5py
import hd5_wrapper


class MatKeyInfo(object):


    def __init__(self,new_var_name,old_var_name,factor):
        self.new_var_name = new_var_name
        self.old_var_name = old_var_name
        self.custom_factor = factor

class Mat_Converter(object):
    '''
    主要用于解析matlab7.3版本以下的mat文件
    '''


    def __init__(self,mat_file_path=None,target_file_path=None,compress_level=6):
        '''

        :param mat_file_path:
        :param target_file_path:
        :param keylist:
        '''
        #mat文件路径
        self.__mat_file_path = mat_file_path
        #读取数据名称集合
        self.__key_list = []
        #生成文件的路径
        self.__target_file_path = target_file_path
        #compress level
        self.__compress_level = compress_level


    @property
    def mat_file_path(self):
        '''

        :return:
        '''
        return self.__mat_file_path

    @mat_file_path.setter
    def mat_file_path(self,mat_file_path):
        '''

        :return:
        '''
        self.__mat_file_path = mat_file_path

    @property
    def target_file_path(self):
        return self.__target_file_path

    @target_file_path.setter
    def target_file_path(self,target_file_path):
        self.__target_file_path = target_file_path

    def yield_data_to_target_file(self):
        '''

        :return:
        '''
        #load the mat file
        matdata = scipy.io.loadmat(self.__mat_file_path)
        #Load the data
        value = matdata['DATA'][0,0]
        # 加载变量名映射表
        json_path = os.getcwd() + r'\convert_table.json'
        with open(json_path, 'r') as json_reader:
            convert_table = json.load(json_reader)
            for x in value.dtype.names:
                if x in convert_table:
                    self.__key_list.append(MatKeyInfo(convert_table[x]['new_name'],x,convert_table[x]['factor']))
        #self.__key_list = [x for x in value.dtype.names]

        #开始生成hdf5
        hf5 = hd5_wrapper.Hd5Wrapper()
        hf5.file_path = self.__target_file_path
        write_data = {}
        sub_data = None
        for key in self.__key_list:
            value_array = value[key.old_var_name] * key.custom_factor
            #print value_array,type(value_array),value_array.shape
            sub_data = hd5_wrapper.Hdf5Data(value_array, self.__compress_level)
            write_data[key.new_var_name] = sub_data
        hf5.data = write_data
        hf5.write_file()
    def _display(self):
        print self.__mat_file_path
        print self.__target_file_path
        print self.__compress_level


class Mat73_Converter(object):
    '''
    用于解析matlab7.3以上的mat文件
    '''

    def __init__(self,mat_file_path=None,target_file_path=None,compress_level=6):
        '''

        :param mat_file_path:
        :param target_file_path:
        :param keylist:
        '''
        #mat文件路径
        self._mat_file_path = mat_file_path
        #读取数据名称集合
        self._key_list = []
        #生成文件的路径
        self._target_file_path = target_file_path
        #compress level
        self._compress_level = compress_level

    @property
    def mat_file_path(self):
        '''

        :return:
        '''
        return self._mat_file_path

    @mat_file_path.setter
    def mat_file_path(self,mat_file_path):
        '''

        :return:
        '''
        self._mat_file_path = mat_file_path

    @property
    def target_file_path(self):
        return self._target_file_path

    @target_file_path.setter
    def target_file_path(self,target_file_path):
        self._target_file_path = target_file_path

    def yield_data_to_target_file(self):
        '''

        :return:
        '''
        #load the mat file
        with h5py.File(self._mat_file_path,'r') as f:
            if 'DATA' in f:
                #Load the data
                value = f['DATA']
                # 加载变量名映射表
                json_path = os.getcwd() + r'\convert_table.json'
                with open(json_path, 'r') as json_reader:
                    convert_table = json.load(json_reader)
                    for x in value.keys():
                        if x in convert_table:
                            self._key_list.append(
                                MatKeyInfo(convert_table[x]['new_name'], x, convert_table[x]['factor']))

                # 开始生成hdf5
                hf5 = hd5_wrapper.Hd5Wrapper()
                hf5.file_path = self._target_file_path
                write_data = {}
                sub_data = None
                for key in self._key_list:
                    value_array = value[key.old_var_name].value.transpose() * key.custom_factor
                    sub_data = hd5_wrapper.Hdf5Data(value_array, self._compress_level)
                    write_data[key.new_var_name] = sub_data
                hf5.data = write_data
                hf5.write_file()


