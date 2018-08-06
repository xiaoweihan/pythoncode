#coding=utf8
import traceback

class Unit_Converter(object):
    '''

    '''

    convert_table = {'n':'N','nm':'N-m','w':'W','kn':'kN','knm':'kN-m','kw':'kW'}

    @classmethod
    def convert_unit(cls,unit_name):

        try:

            #进行小写转换
            convert_unit_name = unit_name.lower()
            #如果存在才进行转换
            if convert_unit_name in cls.convert_table:
                return cls.convert_table.get(convert_unit_name)

            return unit_name

        except BaseException as e:
            print('exception info = {0},traceback = {1}.'.format(str(e), traceback.print_exc()))
            return None



if __name__ == '__main__':

    pass







