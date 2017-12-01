#coding=utf-8

from twisted.internet import protocol,reactor
from time import ctime

class TSServProtocol(protocol.Protocol):
    '''
    implement server by twisted protocol
    '''
    def connectionMade(self):
        '''
        when a client connect call this
        :return:
        '''
        peerclient = self.transport.getPeer().host
        #self.clientList.append(peerclient)

        print 'new client comes.',peerclient
    def dataReceived(self, data):
        '''
        when receive data call this
        :param data:
        :return:
        '''
        self.transport.write('[%s] %s' % (ctime(),data))

    def connectionLost(self, reason):
        print self.transport.client, 'disconnected',reason

if __name__ == '__main__':

    factory = protocol.Factory()
    factory.protocol = TSServProtocol
    print 'waiting for connection...'
    reactor.listenTCP(10024,factory)
    reactor.run()






