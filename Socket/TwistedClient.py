#coding=utf-8
from twisted.internet import protocol,reactor
from time import ctime


class TSClntProtocol(protocol.Protocol):
    def sendData(self):
        data = raw_input('please input the content which you wants to send.')
        if data:
            self.transport.write(data)
        else:
            self.transport.loseConnection()
    def connectionMade(self):
        print 'connect server succeed.'
        self.sendData()

    def dataReceived(self, data):
        print 'received data = ',data
        self.sendData()


class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    clientConnectionLost = clientConnectionFailed = \
        lambda self,connector,reason:reactor.stop()


if __name__ == '__main__':
    reactor.connectTCP('localhost', 10024, TSClntFactory())
    reactor.run()