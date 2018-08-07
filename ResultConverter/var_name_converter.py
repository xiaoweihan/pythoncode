#coding=utf8


class Var_Name_Converter(object):


    '''
    this class implement convert the var name

    '''

    convert_var_name_table = {'Mx':'Mx',
                     'My':'My',
                     'Mz':'Mz',
                     'Fx':'Fx',
                     'Fy':'Fy',
                     'Fz':'Fz',
                     'Dx':'Ux',
                     'Dy':'Uy',
                     'Dz':'Uz',
                     'Rx':'Rx',
                     'Ry':'Ry',
                     'Rz':'Rz',
                     'State pos x':'Px',
                     'State pos y':'Py',
                     'State pos z':'Pz',
                     'State acc x':'Ax',
                     'State acc y':'Ay',
                     'State acc z':'Az',
                     'State vec x':'Vx',
                     'State vec y':'Vy',
                     'State vec z':'Vz',
                     'omega tx':'Wx',
                     'omega ty':'Wy',
                     'omega tz':'Wz',
                     'omegadot tx': 'Qx',
                     'omegadot ty': 'Qy',
                     'omegadot tz': 'Qz'}



    @classmethod
    def convert_var_name(cls,var_name):

        if var_name in cls.convert_var_name_table:
            return cls.convert_var_name_table[var_name]

        #if key not in table return the original name
        return var_name
