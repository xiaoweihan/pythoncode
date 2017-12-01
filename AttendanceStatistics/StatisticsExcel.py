#coding=utf8
import xlwt


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式


    align = xlwt.Alignment()

    align.horz = align.HORZ_CENTER

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
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


    @property
    def excel_name(self):
        return self.__excel_file_name

    @excel_name.setter
    def excel_name(self,strexcel_name):
        self.__excel_file_name = strexcel_name


    def writedatatoexcel(self):
        #创建工作部
        f = xlwt.Workbook()
        sheet = f.add_sheet(u'汇总表', cell_overwrite_ok=True)  # 创建sheet
        #生成考勤汇总表标题
        sheet.write_merge(0, 0, 0, 31, u'考勤汇总表', set_style('Arial', 480, True))  # 第一列
        f.save(self.__excel_file_name)  # 保存文件


if __name__ == '__main__':
    A = ExcelGenerator(r'd:\test.xls')
    A.writedatatoexcel()
