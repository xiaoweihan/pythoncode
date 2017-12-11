#coding=utf8
import time
import random
import doctest
import unittest
import types
import os
import subprocess

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



def Test():
    # f = os.popen('dir D:')
    #
    # for x in f:
    #     print x

    #os.execl(r'd:\TestRunOnPython.exe','xiaowei.han','chong.li')

    result = subprocess.call([u'dir',u'D:\\boost'],shell=True)

    print result

    subprocess.Popen
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

    #A = Myclass()

    Test()

