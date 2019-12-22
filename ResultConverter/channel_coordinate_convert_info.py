#coding=utf8
import numpy as np
import reprlib
import itertools
import compileall
import log
import os
class Channel_Coordinate_Convert_Info(object):
    '''

    '''

    def __init__(self,channel_index,factor,coordinate_name):

        self._channel_index = channel_index
        self._factor = factor
        self._coordinate_name = coordinate_name


    @property
    def channel_index(self):
        return self._channel_index

    @property
    def factor(self):
        return self._factor

    @property
    def coordinate_name(self):
        return self._coordinate_name



def test(x):

    if x > -1:
        return True
    return False



if __name__ == '__main__':

    temp_path = r'b.txt'


    a,b = os.path.split(temp_path)

    print(a,b)

