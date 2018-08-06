#coding=utf8

from Connector import ttypes
from Connector import ResultConverter

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.Thrift import TException
import socket
if __name__ == '__main__':

    try:

        # Make socket
        transport = TSocket.TSocket('127.0.0.1', 10045)

        # Buffering is critical. Raw sockets are very slow
        transport = TTransport.TBufferedTransport(transport)

        # Wrap in a protocol
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        # Create a client to use the protocol encoder
        client = ResultConverter.Client(protocol)

        # Connect!
        transport.open()

        temp_param = ResultConverter.ConvertElement()

        temp_param.strHtcFilePath = r'd:\test_dat\EN121_base_model.htc'
        temp_param.strResultDir = r'd:\test_dat'
        temp_param.strCopyDir = r'd:\test_dat'
        temp_param.costTime = 10.0

        result = client.ConvertResult(temp_param)

        if result:
            print('ok')
        else:
            print('no')

    except TException as tx:
        print(tx.message)
    finally:
        # Close!
        transport.close()