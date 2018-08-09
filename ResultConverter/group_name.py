#coding=utf8

class Group_Name(object):


    group_name_table = {'B1':'B1',
                     'B2':'B2',
                     'B3':'B3',
                     'Twr':'Twr',
                     'Hub':'Hub',
                     'Nac':'Nacelle',
                     'Yaw_Bear':'Yaw bearing'
                     }


    @classmethod
    def convert_group_name(cls,component_name):

        #if key in table

        if component_name in cls.group_name_table:
            return cls.group_name_table[component_name]

        #if key not in table return the original name
        return 'Others'