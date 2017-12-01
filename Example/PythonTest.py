#coding=utf-8

import copy
import struct
import threading
import sys
import threading
import MySQLdb
import time
import socket
import subprocess
import datetime
import time
from twisted.internet import reactor,protocol
from collections import deque
#打印DBAPI信息
'''
print MySQLdb.apilevel
print MySQLdb.threadsafety
print MySQLdb.paramstyle
'''

#connect the mysql
def connectdb(dbAddress,dbPort,dbUser,dbPassword,dbName):
    conn = None
    try:
       conn = MySQLdb.connect(host=dbAddress, port=dbPort, user=dbUser, passwd=dbPassword, charset='utf8', db='testcreate')


       cursor = conn.cursor()
       cursor.execute('select * from test')

       while True:

           Row = cursor.fetchone()
           if not Row:
               break
           print Row
    except:
        print 'connect db failed.'
    else:
        pass
    finally:
        conn.close()





class Circle(object):
    @staticmethod
    def Fun1():
        print 'this is a static method.'

    @classmethod
    def Fun2(cls):
        print 'this is a class method.'

    def __getattr__(self, item):
        print 'call me',item

def Test():

    for x in xrange(10):
        yield x


class Base(object):
    def __init__(self):
        print 'call Base init'

    @classmethod
    def test(cls):
        pass

class Derive(Base):
    def __init__(self):
        super(Derive,self).__init__()

    @classmethod
    def test(cls):
        return cls()



class Person(object):
    def __init__(self,name,age):
        self._name = name
        self._age = age

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self,name):
        self._name = name

    def displayName(self):
        print self._name



def TestCreateFile():
    #组装文件
    strParentDir = r'D:\TestDir'

    for x in range(1,100):
        strFileNameSuffix1 = '%%%03d' % x
        strFileNameSuffix2 = '$%03d' % x
        strFileName1 = strParentDir + '\\' + str(x) + '.' + strFileNameSuffix1
        strFileName2 = strParentDir + '\\' + str(x) + '.' + strFileNameSuffix2
        fp1 = open(strFileName1,'w')
        fp1.write(str(x))
        fp1.close()
        fp2 = open(strFileName2, 'w')
        fp2.write(str(x))
        fp2.close()

    for x in range(4,690):
        strFileNameSuffix1 = '%%%02d' % x
        strFileNameSuffix2 = '$%02d' % x
        strFileName1 = strParentDir + '\\' + str(x) + '.' + strFileNameSuffix1
        strFileName2 = strParentDir + '\\' + str(x) + '.' + strFileNameSuffix2
        fp1 = open(strFileName1, 'w')
        fp1.write(str(x))
        fp1.close()
        fp2 = open(strFileName2, 'w')
        fp2.write(str(x))
        fp2.close()

    for x in xrange(1,101):
        strFileName1 = strParentDir + '\\' + str(x) + '.' + '%AE'
        strFileName2 = strParentDir + '\\' + str(x) + '.' + '$AE'
        strFileName3 = strParentDir + '\\' + str(x) + '.' + '$pj'
        strFileName4 = strParentDir + '\\' + str(x) + '.' + '$PJ'

        fp1 = open(strFileName1, 'w')
        fp1.write(str(x))
        fp1.close()
        fp2 = open(strFileName2, 'w')
        fp2.write(str(x))
        fp2.close()

        fp3 = open(strFileName3, 'w')
        fp3.write(str(x))
        fp3.close()
        fp4 = open(strFileName4, 'w')
        fp4.write(str(x))
        fp4.close()




def TestTime():
    currenttime = time.gmtime()

    strFormat = '%Y-%m-%d %H:%M:%S'

    strcurrenttime = time.strftime(strFormat,currenttime)

    print strcurrenttime

def TestDateTime():
    currenttime = datetime.datetime.now()

    print currenttime
    print type(currenttime)

def TestDeque():
    fifo = deque()


    for x in xrange(1,100):
        fifo.append(x)


    fifo.rotate(1)

    print fifo


if __name__ == '__main__':
    #TestTime()
    #TestDateTime()
    #TestDeque()
    print socket.gethostbyname(socket.gethostname())




