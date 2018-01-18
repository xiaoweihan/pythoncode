#coding=utf8
import os
import multiprocessing
import shutil
import re
import argparse
import mat_parser

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


#文件进行归类
def _sort_files(target_dir):
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
        new_file_name = _filter_file(file_name)
        if new_file_name:
            h5_file_name = os.path.join(kwargs['dir'],new_file_name)

            #查看mat文件版本
            with open(file_name,'r') as f:
                mat_version = f.read(10)

            version = float(mat_version[7:])

            if version >= 7.3:
                matConvert = mat_parser.Mat73_Converter(file_name, h5_file_name, kwargs['compress_level'])
                matConvert.yield_data_to_target_file()
            else:
                matConvert = mat_parser.Mat_Converter(file_name, h5_file_name, kwargs['compress_level'])
                matConvert.yield_data_to_target_file()
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

    # 递归遍历源目录
    mat_file_list = list(_recursive_dir(mat_file_dir,'.mat'))

    # 执行进程的最多个数
    max_process_num = min(multiprocessing.cpu_count(), len(mat_file_list))

    process_arg_array = []

    per_process_arg_num = (len(mat_file_list) + max_process_num - 1) / max_process_num
    x = 0
    for _ in xrange(max_process_num):
        process_tuple = tuple(mat_file_list[x:x + per_process_arg_num])
        x += per_process_arg_num
        tempdict = {}
        tempdict['args'] = process_tuple
        tempdict['dir'] = target_file_dir
        tempdict['compress_level'] = compress_level
        process_arg_array.append(tempdict)

    process_array = []
    for i in xrange(max_process_num):
        p = multiprocessing.Process(target=process_proc, kwargs=process_arg_array[i])
        p.start()
        process_array.append(p)
    for element in process_array:
        element.join()

    _sort_files(target_file_dir)

    print 'congratulations,It is a good job!'

if '__main__' == __name__:
    main()