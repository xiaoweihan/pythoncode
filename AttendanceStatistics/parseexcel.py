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
        self.__excelPath = strPath
        #考勤信息
        self.__AttenceList = []
        #考勤日期
        self.__recordtime = None

    @property
    def excel_path(self):
        return self.__excelPath

    @property
    def record_time(self):
        return self.__recordtime

    @property
    def attence_list(self):
        return self.__AttenceList

    @excel_path.setter
    def excel_path(self,strexcelpath):
        self.__excelPath = strexcelpath

    def ParseExcel(self):
        # 打开员工表的Excel文件
        workbook = xlrd.open_workbook(self.__excelPath)
        # 获取sheet页的个数
        sheetnum = len(workbook.sheet_names())

        if sheetnum < 1:
            return
        # 获取sheet页
        sheetData = workbook.sheet_by_name(u'刷卡记录')

        #解析考勤时间
        self.__recordtime = sheetData.cell(2,2).value


        for i in xrange(4,sheetData.nrows):
            if i % 2 == 0:
                stremployeeID = sheetData.cell_value(i,2)
                stremployeeName = sheetData.cell_value(i,10)
                stremployeeDept = sheetData.cell_value(i,20)
                self.__AttenceList.append(AttenceInfo.AttenceInfo(stremployeeID,stremployeeName,stremployeeDept))
            else:
                for j in xrange(sheetData.ncols):
                    self.__AttenceList[-1].AddAttenceContent(sheetData.cell_value(i,j))

    def display_info(self):

        for element in self.__AttenceList:
            print element.employee_id,element.employee_name,element.employee_dept,element.List

if __name__ == '__main__':
    Parser = parseexcel(ur'D:\汇总表.xls')
    Parser.ParseExcel()
    Parser.display_info()