#coding=utf8
'''
根据员工名单的excel生成json文件
'''
import xlrd
import json
from datetime import date,datetime

class YieldEmployeeList(object):
    '''

    '''
    def __init__(self,excelPath):
        '''

        :param excelPath:
        '''
        self.excelPath = excelPath
        self.employeeList = {}

    def ParseExcel(self):
        '''

        :return:
        '''
        try:
            #打开员工表的Excel文件
            workbook = xlrd.open_workbook(self.excelPath)
            #获取sheet页的个数
            sheetnum = len(workbook.sheet_names())

            if sheetnum < 1:
                return
            #获取sheet页
            sheetData = workbook.sheet_by_index(0)
            for i in range(1,sheetData.nrows):
                for j in range(1,sheetData.ncols):
                    #工号
                    if 1 == j:
                        employeeInfo = {}
                        employeeID = str(int(sheetData.cell_value(i, j)))
                        self.employeeList[employeeID] = employeeInfo
                    else:
                        self.__ParseRowData(i,j,sheetData,workbook,employeeInfo)
        except BaseException,e:
            pass

    def YiledJsonFile(self,jsonFilePath):
        '''

        :param jsonFilePath:
        :return:
        '''
        fp = file(jsonFilePath, 'w')
        jsonContent = json.dumps(self.employeeList,ensure_ascii=False,indent=2)
        fp.write(jsonContent)
        fp.close()

    def __ParseRowData(self,rowindex,colindex,sheetData,workbook,employeeInfo):
        '''

        :param rowindex:
        :param colindex:
        :param sheetData:
        :param workbook:
        :param employeeInfo:
        :return:
        '''
        nTotalCol = sheetData.ncols
        nTotalRow = sheetData.nrows
        if colindex >= nTotalCol or rowindex >= nTotalRow:
            return
        if 2 == colindex:
            employeeInfo['Name'] = sheetData.cell_value(rowindex,colindex)
        elif 3 == colindex:
            employeeInfo['Sex'] = sheetData.cell_value(rowindex,colindex)
        elif 4 == colindex:
            employeeInfo['System'] = sheetData.cell_value(rowindex,colindex)
        elif 5 == colindex:
            employeeInfo['Dept'] = sheetData.cell_value(rowindex,colindex)
        elif 6 == colindex:
            employeeInfo['Catory'] = sheetData.cell_value(rowindex,colindex)
        elif 7 == colindex:
            employeeInfo['Job'] = sheetData.cell_value(rowindex,colindex)
        elif 8 == colindex:
            date_value = xlrd.xldate_as_tuple(sheetData.cell_value(rowindex,colindex), workbook.datemode)
            employeeInfo['JoinTime'] = date_value
        else:
            pass

