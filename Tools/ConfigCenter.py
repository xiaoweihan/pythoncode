#coding=utf-8
from twisted.internet import protocol,reactor
from time import ctime
import time
import logging
import sys
import threading
import json
import os


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


class ConfigContentManager(object):

    __instant = None;
    __lock = threading.Lock();

    def __new__(cls, *args, **kwargs):
        if cls.__instant is None:
            cls.__lock.acquire(True)
            if cls.__instant is None:
                cls.__instant = super(ConfigContentManager,cls).__new__(cls,*args,**kwargs)
            cls.__lock.release
        return cls.__instant

    def __init__(self):
        self.ListenPort = 10024
        self.Lock = threading.Lock()

    def setFilePath(self,configPath):
        self.FilePath = configPath

    def SetListenPort(self,nPort):
        self.ListenPort = nPort
    def GetListenPort(self):
        return self.ListenPort
    #load the json config
    def Load(self):
        result = True
        try:
            self.Content = json.load(file(self.FilePath))
        except BaseException,e:
            result = False
        return  result

    def QueryDataByAddress(self,peerAddress):

        result = None
        self.Lock.acquire(True)
        if peerAddress in self.Content:
            result = json.dumps(self.Content[peerAddress])
        self.Lock.release()
        return result

    Port = property(GetListenPort,SetListenPort)

class ConfigServer(protocol.Protocol):
    '''
    implement server by twisted protocol
    '''
    def connectionMade(self):
        '''
        when a client connect call this
        :return:
        '''
        #get the peer ip address
        peeraddress = self.transport.getPeer().host
        Info_log('[%s] is online.',peeraddress)

    def dataReceived(self, data):
        '''
        when receive data call this
        :param data:
        :return:
        '''
        #if the data equal 1 means get the config
        if data == '1':
            Reader = ConfigContentManager()
            self.transport.write(Reader.QueryDataByAddress(self.transport.getPeer().host))

    def connectionLost(self, reason):
        '''
        when the client close the socket call this
        :param reason:
        :return:
        '''
        peeraddress = self.transport.getPeer().host
        Info_log('[%s] is offline.',peeraddress)

    def responseData(self,peerAddress):
        pass


def main():

    '''
    main function
    :return:
    '''

    #init log module

    Init_log()

    filePath = os.path.abspath(os.getcwd()) + r'\Db.json'
    Reader = ConfigContentManager()
    Reader.setFilePath(filePath)
    Reader.Load()


    factory = protocol.Factory()
    factory.protocol = ConfigServer
    Info_log('waiting for connection...')
    reactor.listenTCP(Reader.Port, factory)
    reactor.run()

if __name__ == '__main__':
    main()









