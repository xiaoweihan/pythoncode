#coding=utf8

'''
load the mat file and convert it's data to txt file
'''
import os
import os.path

import scipy.io
import numpy
import argparse
import hd5_wrapper
import re
class Mat_Converter(object):


    def __init__(self,mat_file_path = None,target_file_path = None,compress_level = 6):
        '''

        :param mat_file_path:
        :param target_file_path:
        :param keylist:
        '''
        #mat文件路径
        self.__mat_file_path = mat_file_path
        #读取数据名称集合
        self.__key_list = None
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
        #load the mat file
        matdata = scipy.io.loadmat(self.__mat_file_path)
        #Load the data
        value = matdata['DATA'][0,0]
        self.__key_list = [x for x in value.dtype.names]


        #开始生成hdf5

        hf5 = hd5_wrapper.Hd5Wrapper()
        hf5.file_path = self.__target_file_path


        write_data = {}
        sub_data = None
        for key in self.__key_list:
            value_array = value[key]
            #print value_array,type(value_array),value_array.shape
            sub_data = hd5_wrapper.Hdf5Data(value_array,self.__compress_level)
            write_data[key] = sub_data
        hf5.data = write_data
        hf5.write_file()
    def _display(self):
        print self.__mat_file_path
        print self.__target_file_path
        print self.__compress_level


#递归遍历某个目录
def _recursive_dir(dir_name,suffix_name):
    '''

    :param dir_name:
    :return:
    '''
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        g = os.walk(dir_name)
        for path, d, filelist in g:
            for filename in filelist:
                matfile_name =  os.path.join(path, filename)
                if os.path.splitext(matfile_name)[1] == suffix_name:
                    yield matfile_name

#过滤文件
def _filter_file(file_name):
    if os.path.exists(file_name) and os.path.isfile(file_name):
        result = re.match('.*_(\d{4}.\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2}.\d{1,2})',file_name)
        if result:
            return result.group(1) + '.h5'
    return None

def main():
    #begin parse the command line
    command_parser = argparse.ArgumentParser(description='show the command usage')
    command_parser.add_argument('--src','-s',help='specific a mat file dir',required=True)
    command_parser.add_argument('--target', '-t', help='specific a target file dir', required=True)
    #command_parser.add_argument('--variable', '-v', help='select variable name', action='append')
    command_parser.add_argument('--compress', '-c', help='set compress level', type=int,choices=range(0,10))
    args = command_parser.parse_args()

    mat_file_dir = args.src
    target_file_dir = args.target
    compress_level = args.compress

    if not os.path.exists(mat_file_dir):
        print mat_file_dir,'is not exist.'
        return
    if not os.path.isdir(mat_file_dir):
        print mat_file_dir,'is not a dir.'
        return

    if not os.path.exists(target_file_dir):
        os.makedirs(target_file_dir)

    #create a parser
    matConvert = Mat_Converter(compress_level=compress_level)
    for element in _recursive_dir(mat_file_dir,'.mat'):
        src_file_name = element
        target_file_name = _filter_file(src_file_name)
        if target_file_name:
            matConvert.mat_file_path = src_file_name
            matConvert.target_file_path = os.path.join(target_file_dir,target_file_name)
            matConvert.yield_data_to_target_file()

    print 'congratulations,It is a good job!'


if '__main__' == __name__:
    main()
