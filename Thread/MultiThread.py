#coding=utf-8
import threading
import time
import random



#thread entry function
def ThreadProc(nSleepSeconds):
    print 'begin sleep ',nSleepSeconds,'...'

    time.sleep(nSleepSeconds)

    print 'end sleep ',nSleepSeconds,'...'



#main function
def main():
    workerThread = threading.Thread(target=ThreadProc,args=(2,))

    print 'begin start a thread,at ',time.ctime()

    workerThread.start()


    time.sleep(10)


    workerThread.join()



    print 'end start a thread at ',time.ctime()



if __name__ == '__main__':
    main()