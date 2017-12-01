#coding=utf-8
'''
this is a log module
'''
import logging
import sys

class Log(object):
    '''
    define a class which is implement the log function
    '''
    def __init__(self,name):
        '''

        '''
        #initialize the log
        self.__initLog(name)

    def __initLog(self,name):
        '''
        :param name:
        :return:
        '''
        self.logger = logging.getLogger(name)
        loggerHandler = logging.StreamHandler(stream=sys.stdout)
        loggerFormat = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
        loggerHandler.setFormatter(loggerFormat)
        loggerHandler.setLevel(logging.DEBUG)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(loggerHandler)

    def info_log(self,msg,*args,**kwargs):
        self.logger.info(msg,*args,**kwargs)

    def debug_log(self,msg,*args,**kwargs):
        self.logger.debug(msg,*args,**kwargs)

    def warn_log(self,msg,*args,**kwargs):
        self.logger.warn(msg,*args,**kwargs)

    def error_log(self,msg,*args,**kwargs):
        self.logger.error(msg,*args,**kwargs)

    def fatal_log(self,msg,*args,**kwargs):
        self.logger.critical(msg,*args,**kwargs)


loggerInstance = Log('Logger')
