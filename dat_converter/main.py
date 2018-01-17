#coding=utf8
'''
use multiprocess convert the dat file to hdf5 files
'''
from dat_file_parser import DatFileParser
import multiprocessing
import argparse
import shutil
import re
import os
import hd5_wrapper
#递归遍历某个目录
def recursive_dir(dir_name,suffix_name):
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
def filter_file(file_name):
    if os.path.exists(file_name) and os.path.isfile(file_name):
        result = re.match('.*(\d{4}.\d{1,2}.\d{1,2}).(\d{1,2}.\d{1,2}.\d{1,2})',file_name)
        if result:
            new_file_name = result.group(1) + '_' + result.group(2) + '.h5'
            return new_file_name
    return None

#文件进行归类
def sort_files(target_dir):
    file_list = os.listdir(target_dir)
    file_sort_type = {}
    for file_name in file_list:
        if os.path.isfile(os.path.join(target_dir,file_name)):
            result = re.match('^(\d{4}.\d{1,2}.\d{1,2})_.*', file_name)
            if result:
                if result.group(1) in file_sort_type:
                    file_sort_type[result.group(1)].append(os.path.join(target_dir,file_name))
                else:
                    file_sort_type[result.group(1)] = []
                    file_sort_type[result.group(1)].append(os.path.join(target_dir, file_name))



    for key in file_sort_type:
        dir_path = os.path.join(target_dir,key)

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)


        for file_name in file_sort_type[key]:
            shutil.move(file_name,dir_path)

#进程函数
def process_proc(**kwargs):
    for file_name in kwargs['args']:
        new_file_name = filter_file(file_name)
        h5_file_name = os.path.join(kwargs['dir'],new_file_name)
        parser = DatFileParser(file_name)
        parser.parse_dat_file()
        hf5 = hd5_wrapper.Hd5Wrapper()
        hf5.file_path = h5_file_name
        write_data = {}
        for elment in parser.get_element_info():
            sub_data = hd5_wrapper.Hdf5Data(elment.data_array, kwargs['compress_level'])
            write_data[elment.var_name] = sub_data
        hf5.data = write_data
        hf5.write_file()

def main():
    #begin parse the command line
    command_parser = argparse.ArgumentParser(description='show the command usage')
    command_parser.add_argument('--src','-s',help='specific a dat file dir',required=True)
    command_parser.add_argument('--target', '-t', help='specific a target file dir', required=True)
    #command_parser.add_argument('--variable', '-v', help='select variable name', action='append')
    command_parser.add_argument('--compress', '-c', help='set compress level', type=int,choices=range(0,10))
    args = command_parser.parse_args()

    #获取到命令行
    dat_file_dir = args.src
    target_file_dir = args.target
    compress_level = args.compress

    #创建目标目录
    if not os.path.exists(target_file_dir):
        os.makedirs(target_file_dir)

    #递归遍历源目录
    dat_file_list = list(recursive_dir(dat_file_dir,'.dat'))

    #执行进程的最多个数
    max_process_num = min(multiprocessing.cpu_count(),len(dat_file_list))

    process_arg_array = []

    per_process_arg_num = (len(dat_file_list) + max_process_num - 1) / max_process_num
    x = 0
    for _ in xrange(max_process_num):
        process_tuple = tuple(dat_file_list[x:x + per_process_arg_num])
        x += per_process_arg_num
        tempdict = {}
        tempdict['args'] = process_tuple
        tempdict['dir'] = target_file_dir
        tempdict['compress_level'] = compress_level
        process_arg_array.append(tempdict)

    process_array = []
    for i in xrange(max_process_num):
        p = multiprocessing.Process(target=process_proc,kwargs=process_arg_array[i])
        p.start()
        process_array.append(p)
    for element in process_array:
        element.join()


    #分组
    sort_files(target_file_dir)

    print 'congratulations,It is a good job!'

if __name__ == '__main__':
    main()