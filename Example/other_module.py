#coding=utf8

import os
import subprocess
import shutil
import matplotlib.pyplot


def run_multi_process(exec_file_name,dir_name,file_num,process_num):
    total_cost = []
    total_file = []
    for x in xrange(process_num):
        temp_dir_name = os.path.join(dir_name,str(x))
        f = subprocess.Popen((exec_file_name, temp_dir_name, file_num), stdout=subprocess.PIPE).stdout
        content = f.readlines()
        f.close()
        for element in content:
            element = element.strip('\r\n')
            subelement = element.split(',')
            strforamt = 'process %s files,cost time %s s.'
            if len(subelement) == 2:
                total_cost.append(subelement[1])
                total_file.append(subelement[0])
                print strforamt % (subelement[0], subelement[1])
    return sum(total_file),max(total_cost)


def run_serial_process(exec_file_name,dir_name,file_num):
    total_cost = []
    total_file = []
    f = subprocess.Popen((exec_file_name, dir_name, file_num), stdout=subprocess.PIPE).stdout
    content = f.readlines()
    f.close()
    for element in content:
        element = element.strip('\r\n')
        subelement = element.split(',')
        strforamt = 'process %s files,cost time %s s.'
        if len(subelement) == 2:
            total_cost.append(subelement[1])
            total_file.append(subelement[0])
            print strforamt % (subelement[0], subelement[1])
    return sum(total_file), max(total_cost)


def run_thread_group_process(exec_file_name,dir_name,file_num):
    total_cost = []
    total_file = []
    f = subprocess.Popen((exec_file_name, dir_name, file_num), stdout=subprocess.PIPE).stdout
    content = f.readlines()
    f.close()
    for element in content:
        element = element.strip('\r\n')
        subelement = element.split(',')
        strforamt = 'process %s files,cost time %s s.'
        if len(subelement) == 2:
            total_cost.append(subelement[1])
            total_file.append(subelement[0])
            print strforamt % (subelement[0], subelement[1])
    return sum(total_file), max(total_cost)


def run_openmp_group_process(exec_file_name,dir_name,file_num):
    total_cost = []
    total_file = []
    f = subprocess.Popen((exec_file_name, dir_name, file_num), stdout=subprocess.PIPE).stdout
    content = f.readlines()
    f.close()
    for element in content:
        element = element.strip('\r\n')
        subelement = element.split(',')
        strforamt = 'process %s files,cost time %s s.'
        if len(subelement) == 2:
            total_cost.append(subelement[1])
            total_file.append(subelement[0])
            print strforamt % (subelement[0], subelement[1])
    return sum(total_file), max(total_cost)

def processfile():
    dir_name = r'D:\H5File\result_hdf5'
    file_list = os.listdir(dir_name)
    for file_name in file_list:
        temp = os.path.splitext(file_name)
        for x in xrange(100):
            temp_file_name = temp[0] + '_' + str(x) + temp[1]
            complete_file_name = os.path.join(dir_name,temp_file_name)
            shutil.copyfile(os.path.join(dir_name,file_name),complete_file_name)

def sort_file():
    dir_name = r'E:\H5File\result_hdf5'
    file_list = os.listdir(dir_name)
    ncount = 0
    ndir = 1
    for file_name in file_list:
        if ncount % 100 == 0:
            temp_dir_name = os.path.join(dir_name,str(ndir))
            os.makedirs(temp_dir_name)
            ndir += 1
        shutil.copyfile(os.path.join(dir_name,file_name),os.path.join(temp_dir_name,file_name))
        ncount += 1

if __name__ == '__main__':
    dir_name = ''
    exec_file_name = ''
    sub_dir_name = ''
    file_num_array = []
    multi_thread_cost = []
    openmp_cost = []
    multi_process_cost = []
    serial_cost = []
    for x in xrange(48,500,48):
        file_num_array.append(x)

    for num in file_num_array:
        element = run_multi_process(exec_file_name,dir_name,num / 48,48)
        multi_process_cost.append(element[1])

        element = run_serial_process(exec_file_name, dir_name,num)
        serial_cost.append(element[1])

        element = run_openmp_group_process(exec_file_name, dir_name, num)
        openmp_cost.append(element[1])

        element = run_thread_group_process(exec_file_name, dir_name, num)
        multi_thread_cost.append(element[1])


    #渲染
    matplotlib.pyplot.plot(file_num_array,multi_thread_cost,label='mult_thread_cost')
    matplotlib.pyplot.plot(file_num_array, openmp_cost, label='openmp_cost')
    matplotlib.pyplot.plot(file_num_array, multi_process_cost, label='mult_process_cost')
    matplotlib.pyplot.plot(file_num_array, serial_cost, label='serial_cost')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.show()











