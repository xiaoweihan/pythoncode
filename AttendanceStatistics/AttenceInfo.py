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

    @property
    def employee_id(self):
        return self.employeeID

    @property
    def employee_name(self):
        return self.employeeName

    @property
    def employee_dept(self):
        return self.employeeDept

