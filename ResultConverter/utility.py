#coding=utf-8
import os


def travel_dir(dir_name):
    '''

    :param dir_name:
    :return:
    :yield file name
    '''

    for dirpath, dirnames, filenames in os.walk(dir_name):

        for file_name in filenames:
            yield os.path.join(dirpath,file_name)




if __name__ == '__main__':
    pass

