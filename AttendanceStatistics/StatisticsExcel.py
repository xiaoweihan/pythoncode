#coding=utf8
import xlwt
import sys
import os
import time
from parseexcel import *


def set_style(name, height, bold=False, just_fit=False):
    style = xlwt.XFStyle()
    align = xlwt.Alignment()
    if just_fit:
        align.horz = align.HORZ_JUSTIFIED
    else:
        align.horz = align.HORZ_CENTER
    align.vert = align.VERT_CENTER
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    # font.color_index = 0x0C
    font.height = height
    style.font = font
    style.alignment = align
    return style

class ExcelGenerator(object):


    def __init__(self,strexcel_name):
        '''
        设置生成Excel文件的名称
        :param strexcel_name:
        '''
        self.__excel_file_name = strexcel_name
        self.__bodylist = []
        self.__recordtime = None

    @property
    def excel_name(self):
        return self.__excel_file_name

    @excel_name.setter
    def excel_name(self,strexcel_name):
        self.__excel_file_name = strexcel_name

    def set_body_list(self,body_list):
        self.__bodylist = body_list

    def set_record_time(self,record_time):
        self.__recordtime = record_time

    def write_title(self,excel_sheet,strdate,ndays):
        '''

        :param excel_sheet:
        :param strdate:
        :return:
        '''
        #格式 工号 姓名 部门 日期
        style1 = set_style(u'宋体', 480, True)
        excel_sheet.write_merge(0, 0, 0, 0 + 3 + ndays - 1, u'考勤汇总表', style1)  # 第一列
        style1 = set_style(u'宋体', 180, True,True)
        excel_sheet.write(1,0,u'考勤日期:',style1)
        excel_sheet.write(1,1,strdate, style1)
        #写 工号 姓名 部门 日期
        title = [u'工号',u'姓名',u'部门']
        style1 = set_style(u'Arial', 160, True,True)
        for nIndex in xrange(3):
            excel_sheet.write(2,nIndex,title[nIndex],style1)
        for dayIndex in xrange(3,3 + ndays):
            excel_sheet.write(2, dayIndex, dayIndex + 1 - 3,style1)

    def write_body(self,excel_sheet):
        '''

        :return:
        '''
        style1 = set_style(u'Arial', 160, False, True)
        nRow = 3
        for element in self.__bodylist:
            if element.employee_id and element.employee_name and element.employee_dept:
                excel_sheet.write(nRow, 0, element.employee_id,style1)
                excel_sheet.write(nRow, 1, element.employee_name,style1)
                excel_sheet.write(nRow, 2, element.employee_dept,style1)
                #写入考勤
                for x in xrange(len(element.List)):
                    excel_sheet.write(nRow, x + 3, element.List[x].decode('utf8'),style1)

                nRow += 1

    def write_excel(self):
        #创建工作簿
        f = xlwt.Workbook()
        sheet = f.add_sheet(u'汇总表', cell_overwrite_ok=True)  # 创建sheet
        #生成考勤汇总表标题
        self.write_title(sheet,self.__recordtime,31)
        self.write_body(sheet)
        f.save(self.__excel_file_name)  # 保存文件
if __name__ == '__main__':




    #获取当前路径

    curdir = os.getcwd()
    excel_file_name = None
    curdir_filelist = os.listdir(curdir)

    for elment in curdir_filelist:
        if elment.endswith('xls') or elment.endswith('xlsx'):
            excel_file_name = curdir.decode('gb2312') + u'\\' + elment.decode('gb2312')
            break
    target_file_name = curdir.decode('gb2312') + ur'\考勤汇总表.xls'
    print u'保存路径为:',target_file_name
    #print u'源文件路径为:',excel_file_name
    #解析excel
    Parser = parseexcel(excel_file_name)
    Parser.ParseExcel()
    list = Parser.attence_list

    excelwriter = ExcelGenerator(target_file_name)
    excelwriter.set_body_list(list)
    excelwriter.set_record_time(Parser.record_time)
    excelwriter.write_excel()
    print u'保存成功!'
    time.sleep(5)