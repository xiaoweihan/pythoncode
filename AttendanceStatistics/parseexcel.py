#coding=utf8
'''
解析考勤的excel文件
'''


import xlrd
import AttenceInfo


class parseexcel(object):
    '''
    解析考勤文件的类
    '''

    def __init__(self,strPath):
        '''

        :param strPath:
        '''
        self.excelPath = strPath
        #考勤信息
        self.AttenceList = []

    def ParseExcel(self):
        # 打开员工表的Excel文件
        workbook = xlrd.open_workbook(self.excelPath)
        # 获取sheet页的个数
        sheetnum = len(workbook.sheet_names())

        if sheetnum < 1:
            return
        # 获取sheet页
        sheetData = workbook.sheet_by_name(u'刷卡记录')


        for i in xrange(4,sheetData.nrows):
            if i % 2 == 0:
                stremployeeID = sheetData.cell_value(i,2)
                stremployeeName = sheetData.cell_value(i,10)
                stremployeeDept = sheetData.cell_value(i,20)
                self.AttenceList.append(AttenceInfo.AttenceInfo(stremployeeID,stremployeeName,stremployeeDept))
            else:
                for j in xrange(1,sheetData.ncols):
                    self.AttenceList[-1].AddAttenceContent(sheetData.cell_value(i,j))

    def YieldAttenceList(self):
        pass

    def YieldAttenceExceptionList(self):
        pass
