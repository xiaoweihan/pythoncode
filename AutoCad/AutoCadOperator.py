#coding=utf-8

from pyautocad import Autocad, APoint

class AutoCadOperator(object):
    '''
    operatorate the autocad soft to generate DWG file
    '''
    def __init__(self):
        #生成的DWG文件的名称(绝对路径)
        self.__strdwgfilename = None
        self.__acd = None

    def initialize(self):
        '''
        初始化
        :return:
        '''
        pass

    def uninitialize(self):
        '''
        反初始化
        :return:
        '''
        pass

    def render_line(self,startpoint,endpoint):
        """
        render a line
        :param pos_x:
        :param pos_y:
        :return:
        """
        pass

    def render_circle(self,centerpoint,radius):
        '''
        render a circle
        :param centerpoint: the coordinate of the circle center
        :param radius: the radius of the circle
        :return:
        '''
        pass

    def render_arc(self,centerpoint,radius,startangle,endangle):
        '''

        :param centerpoint:
        :param radius:
        :param startangle:
        :param endangle:
        :return:
        '''
        pass

    def render_ellipse(self,centerpoint,longAxis,shortAxis):
        '''

        :param centerpoint:
        :param longAxis:
        :param shortAxis:
        :return:
        '''
        pass

    def render_polyline(self,vertexarray):
        '''

        :param vertexarray:
        :return:
        '''
        pass

    def render_text(self,point,strtext,textheight):
        '''

        :param point:
        :param strtext:
        :param textheight:
        :return:
        '''
        pass

    @property
    def dwgfilename(self):
        '''
        get the dwg file name
        :return:
        '''
        return self.__strdwgfilename

    @dwgfilename.setter
    def dwgfilename(self,strname):
        '''
        set the dwg file name
        :param strname:
        :return:
        '''
        self.__strdwgfilename = strname



















if __name__ == '__main__':
    # 连接上autocad
    acad = Autocad(create_if_not_exists=True)

    #获取Document
    acddoc = acad.doc

    acddoc.ActiveLinetype =

