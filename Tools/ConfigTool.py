#coding=utf-8
from twisted.internet import protocol,reactor
from time import ctime
import logging
import sys
import threading
import json
import os
import subprocess
def Init_log():
    '''
    initialize log module
    :return:
    '''
    logger = logging.getLogger()
    loggerHandler = logging.StreamHandler(stream=sys.stdout)
    loggerFormat = logging.Formatter('[%(levelname)s] %(asctime)s %(message)s')
    loggerHandler.setFormatter(loggerFormat)
    loggerHandler.setLevel(logging.NOTSET)
    logger.setLevel(logging.NOTSET)
    logger.addHandler(loggerHandler)

def Info_log(msg,*args,**kwargs):
    logger = logging.getLogger()
    logger.info(msg,*args,**kwargs)

def Debug_log(msg,*args,**kwargs):
    logger = logging.getLogger()
    logger.debug(msg,*args,**kwargs)

def Warn_log(msg,*args,**kwargs):
    logger = logging.getLogger()
    logger.warn(msg,*args,**kwargs)

def Error_log(msg,*args,**kwargs):
    logger = logging.getLogger()
    logger.error(msg,*args,**kwargs)

def Fatal_log(msg,*args,**kwargs):
    logger = logging.getLogger()
    logger.critical(msg,*args,**kwargs)


class ConfigReader(object):

    __instant = None;
    __lock = threading.Lock();

    def __new__(cls, *args, **kwargs):
        if cls.__instant is None:
            cls.__lock.acquire(True)
            if cls.__instant is None:
                cls.__instant = super(ConfigReader,cls).__new__(cls,*args,**kwargs)
            cls.__lock.release
        return cls.__instant

    def __init__(self):
        self.ServerPort = 10024
        self.ServerAddress = None

    def SetServerInfo(self,Address,Port):
        self.ServerAddress = Address
        self.ServerPort = Port
    def GetServerInfo(self):
        return self.ServerAddress,self.ServerPort
    #load the json config
    def Load(self,configPath):
        try:
            Content = json.load(file(configPath))
            self.ServerPort = Content['ServerPort']
            self.ServerAddress = Content['ServerAddress']
        except BaseException,e:
            Error_log(e.message)

    ServerInfo = property(GetServerInfo,SetServerInfo)


class ConfigClient(protocol.Protocol):
    def sendData(self):
        self.transport.write('1')
    def connectionMade(self):
        Info_log('connect server succeed...')
        self.sendData()
    def dataReceived(self, data):
        try:
            self.transport.loseConnection()
            configPath = os.path.abspath(os.getcwd()) + r'\Config.json'
            fp = file(configPath, 'w')
            fp.write(data)
        except BaseException,e:
            Error_log('there is something wrong.')
        else:
            fp.close()

            Info_log('begin start the daemonMaster Process...')
            #start the daemon process
            Arg = []
            daemonPath = os.path.abspath(os.getcwd()) + r'\DaemonMaster.exe'
            #daemonPath = os.path.abspath(os.getcwd()) + r'\TestIO.exe'
            Arg.append(daemonPath)
            subprocess.Popen(Arg, creationflags=subprocess.CREATE_NEW_CONSOLE)
class ConfigClientProxy(protocol.ClientFactory):
    protocol = ConfigClient
    clientConnectionLost = clientConnectionFailed = \
        lambda self,connector,reason:reactor.stop()

def main():

    '''
    main function
    :return:
    '''
    #init log module
    Init_log()

    filePath = os.path.abspath(os.getcwd()) + r'\Tool.json'
    Reader = ConfigReader()
    Reader.Load(filePath)

    Address,Port = Reader.ServerInfo

    reactor.connectTCP(Address, Port, ConfigClientProxy())
    reactor.run()


if __name__ == '__main__':
    main()
