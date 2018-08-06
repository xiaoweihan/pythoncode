#coding=utf8


class Component_Converter(object):

    '''

    '''

    convert_table = {'b1':'B1',
                     'b2':'B2',
                     'b3':'B3',
                     'twr':'Twr',
                     'hub':'Hub'
                     }


    @classmethod
    def convert_Component(cls,component_name):

        #if key in table
        lower_component_name = component_name.lower()

        if lower_component_name in cls.convert_table:
            return cls.convert_table[lower_component_name]

        #if key not in table return the original name
        return component_name