#coding=utf8

from collections import defaultdict

class Group_data_element(object):
    '''

    '''

    def __init__(self):

        #确定当前组有多少元素
        self._group_num = 0
        #确定当前组写的位置
        self._group_write_pos = 0

    @property
    def group_num(self):
        return self._group_num

    @group_num.setter
    def group_num(self,group_num):
        self._group_num = group_num

    @property
    def group_write_pos(self):
        return self._group_write_pos

    @group_write_pos.setter
    def group_write_pos(self, group_write_pos):
        self._group_write_pos = group_write_pos


class Group_data_manager(object):
    '''

    '''

    def __init__(self):

        self._group_dict = defaultdict(lambda : Group_data_element())
    @property
    def group_dict(self):
        return self._group_dict

    def add_group(self,group_name):

        self._group_dict[group_name].group_num += 1

    def write_group(self,group_name):
        self._group_dict[group_name].group_write_pos += 1

    def get_group_write_pos(self,group_name):
        return self._group_dict[group_name].group_write_pos



