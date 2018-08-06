#coding=utf8


class Controller_Info(object):
    '''

    '''


    def __init__(self,controller_name,controller_unit,channel_index,frame_name = None):
        '''

        :param controller_name:
        :param controller_unit:
        '''

        self._channel_index = channel_index
        self._controller_name =  controller_name
        self._controller_unit =  '(' + controller_unit + ')'
        self._frame_name = frame_name

    @property
    def channel_index(self):
        return self._channel_index

    @property
    def controller_name(self):
        return self._controller_name

    @property
    def controller_unit(self):
        return self._controller_unit


    @property
    def frame_name(self):
        return self._frame_name

    @frame_name.setter
    def frame_name(self,frame_name):
        self._frame_name = frame_name


    def __str__(self):
        strcontent = 'channel_index = {0},controller_name = {1},controller_unit = {2}.'
        return strcontent.format(self._channel_index,self._controller_name, self._controller_unit)




