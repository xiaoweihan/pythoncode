#coding=utf8
'''
记录员工的考勤信息
'''


class AttenceInfo(object):
    '''

    '''
    def __init__(self,stremployeeID,strName,strDept):
        #工号
        self.employeeID = stremployeeID
        #姓名
        self.employeeName = strName
        #部门
        self.employeeDept = strDept
        #考勤时间
        self.List = []

    def AddAttenceContent(self,strTime):
        self.List.append(strTime)

    def GetEmployeeName(self):
        return self.employeeName

    def GetEmployeeDept(self):
        return self.employeeDept

    def GetEmployeeID(self):
        return self.employeeID

