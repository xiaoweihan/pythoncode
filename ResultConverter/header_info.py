#coding=utf8

#sel file head info which includes scans,channels,time,format
class Header_Info(object):
    '''
    implement the sel file header info
    '''

    def __init__(self):
        '''

        '''
        #求解器版本ID
        self._versionID = None
        #Time字段
        self._time_info = None
        #Date字段
        self._date_info = None
        #dat文件路径
        self._dat_file_path = None
        #scans
        self._scans = 0
        #channels
        self._channels = 0
        #Time
        self._total_time = 0.0
        #the format of dat file
        self._file_format = 0

    @property
    def version(self):
        '''

        :return:
        '''
        return self._versionID

    @version.setter
    def version(self,version_id):
        self._versionID = version_id

    @property
    def time_info(self):
        '''

        :return:
        '''
        return self._time_info

    @time_info.setter
    def time_info(self,new_time_info):
        '''

        :param new_time_info:
        :return:
        '''
        self._time_info = new_time_info


    @property
    def date_info(self):
        '''

        :return:
        '''
        return self._date_info


    @date_info.setter
    def date_info(self,new_date_info):
        '''

        :param new_date_info:
        :return:
        '''
        self._date_info = new_date_info


    @property
    def dat_file_path(self):
        '''

        :return:
        '''
        return self._dat_file_path


    @dat_file_path.setter
    def dat_file_path(self,new_dat_file_path):
        '''

        :param new_dat_file_path:
        :return:
        '''
        self._dat_file_path = new_dat_file_path

    @property
    def scans(self):
        '''

        :return:
        '''
        return self._scans

    @scans.setter
    def scans(self,new_scans):
        '''

        :param new_scans:
        :return:
        '''
        self._scans = new_scans


    @property
    def channels(self):
        '''

        :return:
        '''
        return self._channels

    @channels.setter
    def channels(self,new_channels):
        '''

        :param new_channels:
        :return:
        '''
        self._channels = new_channels


    @property
    def total_time(self):
        '''

        :return:
        '''
        return self._total_time


    @total_time.setter
    def total_time(self,new_total_time):
        '''

        :param new_total_time:
        :return:
        '''
        self._total_time = new_total_time


    @property
    def file_format(self):
        '''

        :return:
        '''
        return self._file_format

    @file_format.setter
    def file_format(self,new_file_format):
        '''

        :param new_file_format:
        :return:
        '''
        self._file_format = new_file_format


    def __str__(self):
        '''

        :return:
        '''
        strContent = 'Version ID = {0},Time = {1},Date = {2},Result file = {3},Scans = {4},Channels = {5},Time [sec] = {6},Format = {7}'

        return strContent.format(self._versionID,self._time_info,self._date_info,self._dat_file_path,self._scans,
                                 self._channels,self._total_time,self._file_format)