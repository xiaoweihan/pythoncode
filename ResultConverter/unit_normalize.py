#coding=utf8
import math

class Unit_Normalizer(object):


    convert_table = {'(km)':{'name':'(m)','factor':1e3},
                     '(deg)':{'name':'(rad)','factor':(math.pi / 180.0)},
                     '(km/h)':{'name':'(m/s)','factor':(1.0/3.6)},
                     '(deg/s)':{'name':'(rad/s)','factor':(math.pi / 180.0)},
                     '(rpm)':{'name':'(rad/s)','factor':(math.pi / 30)},
                     '(deg/s^2)':{'name':'(rad/s^2)','factor':(math.pi / 180.0)},
                     '(kN)':{'name':'(N)','factor':1e3},
                     '(MN)': {'name': '(N)', 'factor': 1e6},
                     '(kN-m)': {'name': '(N-m)', 'factor': 1e3},
                     '(MN-m)': {'name': '(N-m)', 'factor': 1e6},
                     '(g)': {'name': '(kg)', 'factor': 1e-3},
                     '(g/cm^3)': {'name': '(kg/m^3)', 'factor': 1e3},
                     '(kW)': {'name': '(W)', 'factor': 1e3},
                     '(MW)': {'name': '(W)', 'factor': 1e6},
                     '(kPa)': {'name': '(Pa)', 'factor': 1e3},
                     '(Mpa)': {'name': '(kg/m^3)', 'factor': 1e3},
                     '(ms)': {'name': '(s)', 'factor': 1e-3}
    }


    @classmethod
    def normalize_unit(cls,unit_name):

        '''

        :param unit_name:
        :return: new unit name and the transfer factor
        '''
        if unit_name in cls.convert_table:
            return cls.convert_table[unit_name]['name'],cls.convert_table[unit_name]['factor']

        #如果不存在，则返回原来的单位及系数为1.0
        return unit_name,1.0


if __name__ == '__main__':


    unit_name,factor = Unit_Normalizer.normalize_unit('(rad/s^2)')

    print(unit_name,factor)

