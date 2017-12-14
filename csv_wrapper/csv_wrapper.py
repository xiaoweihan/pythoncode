#coding=utf8

'''
this is encapsulate the csv module

copyright:xiaowei.han reserved.




'''


#作者
__author__ = 'xiaowei.han'
#版本号
__version__ = 1.0

import csv

class Abstract_Wrapper(object):
    '''

    '''
    def __init__(self,csv_file_name=None):
        '''

        :param csv_file_name:
        '''
        #set the csv file name
        self.__csv_file_name = csv_file_name

    @property
    def csv_file_name(self):
        return self.__csv_file_name

    @csv_file_name.setter
    def csv_file_name(self,csv_file_path):
        self.__csv_file_name = csv_file_path


    def read_csv(self):
        '''

        :return:
        '''
        with open(self.__csv_file_name,'rb',encoding='utf-8') as f:
            return csv.reader(f)


    def write_csv(self,write_data):
        '''

        :return:
        '''
        with open(self.__csv_file_name,'w') as f:
            writer = csv.writer(f)
            for element in write_data:
                writer.writerow(element)



class CSV_Wrapper(Abstract_Wrapper):
    '''

    '''

    def read_csv(self):
        pass







class CSV_DictWrapper(Abstract_Wrapper):

    def read_csv(self):
        '''

        :return:
        '''
        pass

    def write_csv(self):
        '''

        :return:
        '''
        pass





