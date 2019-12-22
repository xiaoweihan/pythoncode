#coding=utf8


class Channel_Info(object):

    '''

    '''

    def __init__(self,var_name,component_name,frame_name,var_unit,section_name,channel_index,group_name):

        self._var_name = var_name
        self._component_name = component_name
        self._frame_name = frame_name
        self._var_unit = '(' + var_unit + ')'
        self._section_name = section_name
        #从1开始
        self._channel_index = channel_index

        self._group_name = group_name

    @property
    def var_name(self):
        return self._var_name

    @property
    def var_unit(self):
        return self._var_unit

    @property
    def component_name(self):
        return self._component_name

    @property
    def frame_name(self):
        return self._frame_name

    @property
    def section_name(self):
        return self._section_name

    @property
    def channel_index(self):
        return self._channel_index


    @property
    def group_name(self):
        return self._group_name

    def __str__(self):

        strcontent = 'channel_index = {0},var_name = {1},component_name = {2},frame_name = {3},var_unit = {4},section_name = {5}.'

        return  strcontent.format(self._channel_index,self._var_name,self._component_name,self._frame_name,self._var_unit,self._section_name)
