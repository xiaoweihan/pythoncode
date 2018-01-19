#coding=utf8

'''
implement the log which is used to log some info
'''
import os
import logging
import shutil
import sys
import logging.handlers

class LogWrapper(object):

    def __init__(self,log_file_dir,log_file_name,log_level=logging.DEBUG,output_file=False):
        '''

        :param log_dir:
        :param log_name:
        :param max_file_size:
        '''
        logging.getLogger().setLevel(logging.NOTSET)
        self._logger = logging.getLogger(__name__)
        #确定输出为file
        if output_file:
            # 判断日志目录是否存在
            if not os.path.exists(log_file_dir):
                # 创建日志目录
                os.makedirs(log_file_dir)
            new_log_file_name = os.path.join(log_file_dir,log_file_name)
            log_file_handler = logging.handlers.TimedRotatingFileHandler(new_log_file_name,'S',1)
            log_file_handler.suffix = '%Y-%m-%d.log'
            log_file_handler.setLevel(log_level)

            log_file_fmt = '[%(levelname)s] %(asctime)s [%(module)s] %(message)s'
            log_file_formatter = logging.Formatter(log_file_fmt)
            log_file_handler.setFormatter(log_file_formatter)

            self._logger.addHandler(log_file_handler)
        else:
            log_console_handler = logging.StreamHandler(sys.stdout)
            log_console_handler.setLevel(log_level)
            log_console_fmt = '[%(levelname)s] %(asctime)s [%(module)s] %(message)s'
            log_console_formatter =  logging.Formatter(log_console_fmt)
            log_console_handler.setFormatter(log_console_formatter)
            self._logger.addHandler(log_console_handler)


    def info_log(self,msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def debug_log(self,msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def warn_log(self,msg, *args, **kwargs):
        self._logger.warn(msg, *args, **kwargs)

    def error_log(self,msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def fatal_log(self,msg, *args, **kwargs):
        logging.getLogger(__name__).critical(msg, *args, **kwargs)


