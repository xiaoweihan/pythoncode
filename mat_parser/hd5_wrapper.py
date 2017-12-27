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
        #判断是否是一个Group
        if not hasattr(self._hdf5_file[node_name],'visit'):
           self._data_dict[node_name] = self._hdf5_file[node_name].value


class Hdf5Data(object):

    def __init__(self,data=None,compress_level=6,*kdim):
        self.__dim = kdim
        self.__data = data
        self.__compress_level = compress_level

    @property
    def data(self):
        return self.__data

    @property
    def compress_level(self):
        return self.__compress_level

    @property
    def dim(self):
        return self.__dim


class Hd5Wrapper(object):
    '''
    implments read and write hdf5 format file
    '''

    def __init__(self):
        self.__file_path = None
        #数据
        self.__data = {}
        self.__compress_level = 4

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
    def compress_level(self):
        return self.__compress_level

    @compress_level.setter
    def compress_level(self,level):
        self.__compress_level = level

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
        pass
        # try:
        #     root = h5py.File(self.__file_path,'r')
        #     root.visit(_VisitGroup(self.__data, root))
        # except BaseException,e:
        #     raise
        # finally:
        #     root.close()


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
                group_object.create_dataset(key,data=dict_object[key].data,chunks=True,compression='gzip',compression_opts=dict_object[key].compress_level)

def main():
    def write_file():
        '''

        :return:
        '''

        A = numpy.array([[1,2,3,4],[4,5,6,7],[6,7,8,9]])

        tempdata = Hdf5Data(A,6)

        write_content = {}
        write_content['河北'] = tempdata


        person_name = ['xww','s','d']

        tempdata = Hdf5Data(person_name, 6, 3, 3)

        write_content['江苏'] = tempdata


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