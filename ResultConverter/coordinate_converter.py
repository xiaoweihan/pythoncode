#coding=utf8


class Coordinate_Converter(object):

    '''

    '''


    global_coord_convert_table = {'y':{'factor':1,'name':'x'},
                                  'x':{'factor':1,'name':'y'},
                                  'z': {'factor': -1, 'name': 'z'}
                                  }


    tower_coord_convert_table = {'y':{'factor':1,'name':'x'},
                                 'x':{'factor':-1,'name':'y'},
                                 'z': {'factor': 1, 'name': 'z'}
                                }

    shaft_coord_convert_table = {'y':{'factor':1,'name':'z'},
                                 'x':{'factor':-1,'name':'y'},
                                 'z': {'factor': -1, 'name': 'x'}
                                }

    nonrotating_shaft_coord_convert_table = {'y':{'factor':1,'name':'z'},
                                             'x':{'factor':-1,'name':'y'},
                                             'z': {'factor': -1, 'name': 'x'}
                                            }


    blade_shaft_coord_convert_table = {'y':{'factor':1,'name':'x'},
                                       'x':{'factor':-1,'name':'y'},
                                       'z': {'factor': 1, 'name': 'z'}
                                      }

    hub_shaft_coord_convert_table = {'y':{'factor':1,'name':'x'},
                                     'x':{'factor':-1,'name':'y'},
                                     'z': {'factor': 1, 'name': 'z'}
                                    }

    convert_table = {'G':global_coord_convert_table,'T':tower_coord_convert_table,
                     'R':shaft_coord_convert_table,'N':nonrotating_shaft_coord_convert_table,
                     'B':blade_shaft_coord_convert_table,'H':hub_shaft_coord_convert_table}


    @classmethod
    def convert_coordinate(cls,frame_name,var_name):
        '''

        :param frame_name:
        :return:
        '''

        #如果Frame_name在表中
        if frame_name in cls.convert_table:
            #获取varname的后缀名
            var_name_suffix = var_name[-1].lower()
            if var_name_suffix in cls.convert_table[frame_name]:
                #组合成新的名字

                if var_name[-1].islower():
                    new_var_name = var_name[:-1] + cls.convert_table[frame_name][var_name_suffix]['name']
                else:
                    new_var_name = var_name[:-1] + cls.convert_table[frame_name][var_name_suffix]['name'].upper()


                return cls.convert_table[frame_name][var_name_suffix]['factor'], new_var_name
        return 1.0,var_name



