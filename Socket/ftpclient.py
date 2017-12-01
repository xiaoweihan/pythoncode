#coding=utf-8


import ftplib
import os



class FtpCallBack(object):
    def __init__(self,fileName):
        self.FileName = fileName
        self.fp = open(self.FileName,'wb')

    def WriteData(self, data):
        if self.fp:
            self.fp.write(data)

    def __del__(self):
        if self.fp:
            self.fp.close()





def VisitDir(Dir,FtpClient,DirArray):

    lstArray = FtpClient.nlst(Dir)


    if len(lstArray) == 0:
        DirArray.append(Dir)
    else:
        VisitDir(Dir,FtpClient,DirArray)




def IsDir(strcontent):
    if strcontent[0] == 'd':
        return True

    else:
        return False







if __name__ == '__main__':

    FtpClient = None
    try:
        FtpClient = ftplib.FTP(host='172.16.71.99')
        FtpClient.login('xiaowei.han','123456')
        listArray = []

        content = FtpClient.dir()

        print type(content)







        #FtpClient.cwd('MPI')

        #begin download a file

        #cb = FtpCallBack(r'D:\text.pdf').WriteData
        #FtpClient.retrbinary('RETR mpich2-1.4-installguide.pdf',cb)


    except BaseException,e:
        print 'open ftp failed.',e.message

    finally:

        if FtpClient:
            FtpClient.close()


