#coding=utf-8

'''
this is the main function
'''

#import some modules or packages
from log import loggerInstance
from ExecDynamicCodeTool import SingletonObj

def main():
    '''
    deffine the main function
    :return:
    '''
    codepath = raw_input('please input the code file path:')

    if SingletonObj.RunCode(codepath):
        loggerInstance.debug_log('run succeed.')
    else:
        loggerInstance.debug_log('run failed.')


if __name__=='__main__':
    main()