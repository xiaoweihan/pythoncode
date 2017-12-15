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
        self.csv_file_name = csv_file_name

    def read_csv(self):
        pass

    def write_csv(self,write_data):
        pass


class CSV_Wrapper(Abstract_Wrapper):
    '''

    '''

    def read_csv(self):
        '''

        :return:


        :yield

        :raise
        '''
        #read_data = []
        with open(self.csv_file_name,'rb') as f:
            for data in csv.reader(f):
                #read_data.append(data)
                yield data

        #return read_data
    def write_csv(self,write_data):
        '''

        :return:
        '''
        with open(self.csv_file_name,'wb') as f:
            writer = csv.writer(f)
            for element in write_data:
                writer.writerow(element)

class CSV_DictWrapper(Abstract_Wrapper):

    def read_csv(self):
        '''

        :return:
        '''
        with open(self.csv_file_name,'rb') as f:
             for data in csv.DictReader(f):
                 yield data

    def write_csv(self,fild_names,write_data):
        '''

        :return:
        '''
        with open(self.csv_file_name,'wb',) as f:
            dict_writer = csv.DictWriter(f,fild_names)

            dict_writer.writeheader()

            for element in write_data:
                dict_writer.writerow(element)




#only just for test

def test_write_csv_wrapper():
    csv_file_name = r'D:\only.csv'
    common_csv_operator = CSV_Wrapper(csv_file_name)
    write_data = [['xiaowei.han',32],['chong.lin',34],['lun.wang',36]]
    common_csv_operator.write_csv(write_data)

def test_read_csv_wrapper():
    csv_file_name = r'D:\only.csv'
    common_csv_operator = CSV_Wrapper(csv_file_name)
    for element in common_csv_operator.read_csv():
        print element

def test_write_dict_csv_wrapper():
    csv_file_name = r'D:\only_dict.csv'
    common_csv_operator = CSV_DictWrapper(csv_file_name)
    #write_data = [['xiaowei.han', 32], ['chong.lin', 34], ['lun.wang', 36]]
    #common_csv_operator.write_csv(write_data)

    write_data = [{'first_name':12,'second_name':33},{'first_name':7655,'second_name':987}]
    common_csv_operator.write_csv(['first_name','second_name'],write_data)


if __name__ == '__main__':

    test_write_csv_wrapper()
    #test_read_csv_wrapper()
    test_write_dict_csv_wrapper()





