#coding=utf8


import xlrd
import json
import struct

def main():

    xls_path = r'D:\table.xlsx'
    json_path = r'D:\convert_table.json'

    convert_table = {}
    # 打开员工表的Excel文件
    workbook = xlrd.open_workbook(xls_path)
    # 获取sheet页的个数
    sheetnum = len(workbook.sheet_names())

    if sheetnum < 1:
        return

    # 获取sheet页
    sheetData = workbook.sheet_by_index(0)

    # 解析考勤时间
    row_num = sheetData.nrows
    col_num = sheetData.ncols

    for x in xrange(1,row_num):
        old_name = sheetData.cell_value(x,0)
        new_name = sheetData.cell_value(x,1)

        old_name = old_name.encode('utf8')
        new_name = new_name.encode('utf8')

        tempobj = {}

        tempobj['new_name'] = new_name
        tempobj['factor'] = 1

        convert_table[old_name] = tempobj

    with open(json_path,'w') as fwriter:

        json.dump(convert_table,fwriter)

if __name__ == '__main__':
    #main()


    a = 12.34

    # 将a变为二进制
    fmt = 'i'
    bytes = struct.pack(fmt, a)
