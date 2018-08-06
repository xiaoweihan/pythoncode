#coding=utf8

class Frame_Converter(object):

    '''
    this class implement convert the frame name

    '''

    convert_table = {'blade1':'B',
                     'blade2':'B',
                     'blade3':'B',
                     'global':'G',
                     'tower':'T',
                     'shaft':'R',
                     'nonrotating_shaft':'N',
                     'hub1':'H',
                     'hub2':'H',
                     'hub3':'H'}


    @classmethod
    def convert_frame(cls,frame_name):

        #if key in table
        lower_frame_name = frame_name.lower()

        if lower_frame_name in cls.convert_table:
            return cls.convert_table[lower_frame_name]

        #if key not in table return the original name
        return frame_name





if __name__ == '__main__':

    frame_name = 'hub123'

    print(Frame_Converter.convert_frame(frame_name))