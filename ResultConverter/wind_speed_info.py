#coding=utf8


class WindSpeedInfo(object):

    '''
    this class implement the wind speed info

    '''

    def __init__(self,speed_name,speed_unit,channel_index,frame_name,group_name):
        '''

        '''
        self._channel_index = channel_index
        self._wind_speed_name = speed_name
        self._wind_speed_unit = '(' + speed_unit + ')'
        self._frame_name = frame_name

        #所在的分组信息
        self._group_name = group_name

    @property
    def channel_index(self):
        return self._channel_index

    @property
    def wind_speed_name(self):
        return self._wind_speed_name

    @wind_speed_name.setter
    def wind_speed_name(self,wind_speed_name_info):
        self._wind_speed_name = wind_speed_name_info

    @property
    def wind_speed_unit(self):
        return self._wind_speed_unit

    @wind_speed_unit.setter
    def wind_speed_unit(self,wind_speed_unit_info):
        self._wind_speed_unit = wind_speed_unit_info

    @property
    def frame_name(self):
        return self._frame_name

    @frame_name.setter
    def frame_name(self,frame_name):
        self._frame_name = frame_name

    @property
    def group_name(self):
        return self._group_name


    def __str__(self):
        strcontent = 'channel_index = {0},wind_speed_name = {1},wind_speed_unit = {2},frame_name = {3}.'
        return strcontent.format(self._channel_index,self._wind_speed_name,self._wind_speed_unit,self._frame_name)