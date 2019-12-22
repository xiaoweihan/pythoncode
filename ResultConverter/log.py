#coding=utf-8
'''
this is a log module
'''
import logging
import logging.handlers
import sys

class Log(object):
    '''
    define a class which is implement the log function
    '''
    def __init__(self,name):
        '''

        '''
        #initialize the log
        self._initLog(name)

    def _initLog(self,name):
        '''
        :param name:
        :return:
        '''
        self.logger = logging.getLogger(name)
        #建立一个控制台输出的处理
        logger_console_Handler = logging.StreamHandler(stream=sys.stdout)
        loggerFormat = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
        logger_console_Handler.setFormatter(loggerFormat)
        logger_console_Handler.setLevel(logging.DEBUG)

        #建立一个文件的输出处理器
        logger_file_Handler = logging.handlers.TimedRotatingFileHandler('result_converter','D')

        logger_file_Handler.setFormatter(loggerFormat)
        logger_file_Handler.setLevel(logging.DEBUG)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logger_console_Handler)
        self.logger.addHandler(logger_file_Handler)

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
