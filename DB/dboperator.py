'''
operator db eg. mysql oracle sqlserver sqllist3
now implement operator the mysql

'''
#coding=utf8

from MySQLdb import *

__metaclass__=type

class abstractdbInterface:
    '''
    define the operate db interface this is abstract class.
    '''
    def __init__(self):
        self.dbAddress = None
        self.dbPort = None
        self.dbUser = None
        self.dbPasswd = None
    def setdbAddress(self,dbAddress):
        '''
        set the db address
        :param dbAddress:
        :return:
        '''
        self.dbAddress = dbAddress
    def setdbPort(self,dbPort):
        '''
        set the db port
        :param dbPort:
        :return:
        '''
        self.dbPort = dbPort
    def setdbUser(self,dbUser):
        '''
        set the db user
        :param dbUser:
        :return:
        '''
        self.dbUser = dbUser
    def setdbPasswd(self,dbPasswd):
        '''
        set the db user's password
        :param dbPasswd:
        :return:
        '''
        self.dbPasswd = dbPasswd

    def opendb(self):
        '''
        connect the db server
        :return:
        '''
        pass

    def closedb(self):
        '''
        close the db server
        :return:
        '''
        pass

    def executeNoquerySQL(self,strSQL):
        '''
        execute the sql which is not query
        :param strSQL:
        :return:
        '''
        pass

    def executeQuerySQL(self,strSQL):
        '''
        execute the query sql
        :param strSQL:
        :return:
        '''
        pass

class mysqlInterface(abstractdbInterface):
    '''
    operator the mysql
    '''

    def __init__(self):
        super(mysqlInterface,self).__init__()
        self.conn = None
        self.dbInstance = None


    def setDbInstance(self,strDbInstance):
        '''

        :param strDbInstance:
        :return:
        '''
        self.dbInstance = strDbInstance

    def opendb(self):
        '''
        connect the db server
        :return: True succeed False failed
        '''
        bResult = True
        try:
            self.conn = connect(host=self.dbAddress, port=self.dbPort, user=self.dbUser, passwd=self.dbPasswd, charset='utf8', db=self.dbInstance)
        except BaseException,e:
            print 'connect dbserver failed.',e.message
            bResult = False
        return bResult

    def closedb(self):
        '''
        close the db server
        :return:
        '''
        try:
            self.conn.close()
        except BaseException,e:
            print 'disconnect dbserver failed.', e.message

    def executeNoquerySQL(self, strSQL):
        '''
        execute the sql which is not query
        :param strSQL:
        :return:
        '''
        try:
            dbCursor = self.conn.cursor()
            dbCursor.execute(strSQL)
        except BaseException,e:
            print 'executeNoquerySQL failed.', e.message
        finally:
            dbCursor.close()

    def executeQuerySQL(self, strSQL):
        '''
        execute the query sql
        :param strSQL:
        :return: return a list which eleme is a tuple
        '''
        result = []
        try:
            dbCursor = self.conn.cursor()
            dbCursor.execute(strSQL)
            for rowdata in dbCursor.fetchall():
                result.append(rowdata)
        except BaseException,e:
            print 'executeQuerySQL failed.', e.message
        finally:
            dbCursor.close()

        return result

def UnitTestFunction():

    db = mysqlInterface()
    db.setdbAddress('127.0.0.1')
    db.setdbPort(3306)
    db.setdbUser('root')
    db.setdbPasswd('admin')
    db.setDbInstance('testcreate')

    if db.opendb():
        result = db.executeQuerySQL('select * from test')

        for data in result:
            print data

        db.closedb()
#Test Demo
if '__main__' == __name__:
    UnitTestFunction()