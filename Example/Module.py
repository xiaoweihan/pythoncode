#coding=utf8
import time
import random
import doctest
import unittest
import types
import os
import subprocess
import numpy
import random
import csv
from collections import namedtuple
def test_fun():
    yield 1
    print 'pause'
    yield 2

def counter(start_at=0):
    count = start_at
    while True:
        val = (yield  count)
        if val is not None:
            count = val
        else:
            count += 1

class Myclass(object):


    def display(self):
        print self.__class__.__name__

    def change(self):
        self.__class__ = type(1)

    def __init__(self):
        self.__name = 'abc'



def Test():
    # f = os.popen('dir D:')
    #
    # for x in f:
    #     print x

    #os.execl(r'd:\TestRunOnPython.exe','xiaowei.han','chong.li')

    result = subprocess.call([u'dir',u'D:\\boost'],shell=True)

    print result


def test_numpy():

    num_array = numpy.array([[1,2,3],[4,5,6]],dtype=numpy.int32)

    print num_array

    print num_array.T

def test_matplotlib():

    import matplotlib.pyplot as plt
    x_axis_var = numpy.linspace(0,2 * 3.14,100)
    y_axis_var_sin = numpy.exp(x_axis_var)

    y_axis_var_cos = numpy.cos(x_axis_var)
    #plt.plot(x_axis_var,y_axis_var_sin)
    plt.plot(x_axis_var, y_axis_var_cos,'r*-')
    plt.ylabel('cos')
    plt.show()

def test_csv(csvtempfile):
    with open(csvtempfile, 'wb') as csvfile:
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

if __name__ == '__main__':
    # test_iter = counter(5)
    #
    # print 'begin'
    #
    # print  test_iter.next()
    #
    # print  test_iter.next()
    #
    # test_iter.send(100)
    #
    # print  test_iter.next()
    #
    # print  test_iter.next()
    #
    # print 'end'
    #test_numpy()
    #test_matplotlib()
    #test_csv(r'd:\a.csv')

    person = namedtuple('ssss',['age','tel'])


    A = person(age=22,tel='15261850264')


    print A,type(A)