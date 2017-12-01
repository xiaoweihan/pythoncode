#coding=utf-8
'''
execute the python code or algorithm which other progarmmer writes
'''

class ExecDynamicCodeTool(object):
    '''

    '''
    def RunCode(self,codepath):
        '''
        run the code
        :param codepath:
        :return:
        '''
        fp = None
        try:
            fp = open(codepath,'r')
            codecontent = fp.read()
            codeobject = compile(codecontent,'','exec')
            exec codeobject
            return True
        except BaseException,e:
            return False
        finally:
            if fp:
                fp.close()



SingletonObj = ExecDynamicCodeTool()