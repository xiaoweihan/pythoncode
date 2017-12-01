#coding=utf8
'''
CopyRight:
Description:wrap the h5py module
author:xiaowei.han
'''
import types
import exceptions
import h5py
import numpy

class _VisitGroup(object):
    '''
    visit the hdf5 group callable object
    '''

    def __init__(self,data_dict,hdf5_file):
        self._data_dict = data_dict
        self._hdf5_file = hdf5_file

    def __call__(self, node_name):
        if not hasattr(self._hdf5_file[node_name],'visit'):
           self._data_dict[node_name] = self._hdf5_file[node_name].value

class Hd5Wrapper(object):
    '''
    implments read and write hdf5 format file
    '''

    def __init__(self):
        self.__file_path = None
        #数据
        self.__data = {}

    @property
    def file_path(self):
        '''

        :return:
        '''
        return self.__file_path

    @file_path.setter
    def file_path(self,str_file_path):
        '''

        :param str_file_path:
        :return:
        '''
        self.__file_path = str_file_path

    @property
    def data(self):
        '''

        :return:
        '''
        return self.__data

    @data.setter
    def data(self,write_data):
        '''

        :param write_data:
        :return:
        '''
        if type(write_data) is types.DictType:
            self.__data = write_data
        else:
            raise exceptions.TypeError

    def read_file(self):
        try:
            root = h5py.File(self.__file_path,'r')
            root.visit(_VisitGroup(self.__data, root))
        except BaseException,e:
            raise
        finally:
            root.close()


    def write_file(self):

        try:
            root = h5py.File(self.__file_path, 'w')
            self._recursive_create_group(root,self.__data)
        except BaseException,e:
            raise
        finally:
            root.flush()
            root.close()

    def display_content(self):
        '''

        :return:
        '''
        for key, value in self.__data.items():
            print key, value, type(value)
    def _recursive_create_group(self,group_object,dict_object):
        for key, value in dict_object.items():
            # 判断值是不是dict
            if type(value) is types.DictType:
                sub_group = group_object.create_group(key)
                self._recursive_create_group(sub_group,dict_object[key])
            else:
                group_object.create_dataset(key,data=dict_object[key])

def main():
    def write_file():
        '''

        :return:
        '''
        A = numpy.array([[1,2,3,4],[4,5,6,7],[6,7,8,9]])
        write_content = {}
        write_content['河北'] = A
        write_content['jiangsu'] = ['hanxiaowie','dddd','ssss']
        sub_content = {}
        sub_content['wuhan'] = numpy.arange(23)
        write_content['hubei'] = sub_content
        sub_content = {}
        sub_content['hangzhou'] = numpy.arange(200)
        write_content['zhejiang'] = sub_content
        wrapper = Hd5Wrapper()
        wrapper.file_path = r'd:\foo1.h5'
        wrapper.data = write_content
        wrapper.write_file()
    def read_file():
        '''

        :return:
        '''
        wrapper = Hd5Wrapper()
        wrapper.file_path = r'd:\foo1.h5'
        wrapper.read_file()
        wrapper.display_content()

    write_file()
    #read_file()

if '__main__' == __name__:
    main()