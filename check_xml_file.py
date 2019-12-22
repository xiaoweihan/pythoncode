#  -*- endcoding : utf8 -*-
'''
@File : check_xml_file

@Author: xiaowei.han

@Date : 2019/12/22

@Desc :
'''

import os
import sys
import xml.etree.cElementTree as ET



def check_xml_file(xml_file_path):
    '''

    :param xml_file_path:
    :return:
    '''
    if not os.path.exists(xml_file_path):
        print('{0} is not exist.'.format(xml_file_path))
        return False


    try:
        TreeRoot = ET.parse(xml_file_path)

    except ET.ParseError as e:
        print('parse {0} cause exception {1}.'.format(xml_file_path,e.msg))
        return False

    return True

if __name__ == '__main__':
    '''
    '''

    if len(sys.argv) != 2:
        print('the input param invalid.')
        sys.exit(1)

    xml_file_path = sys.argv[1]

    if check_xml_file(xml_file_path):
        print('the xml file style is right.')
    else:
        print('the xml file style is wrong.')

    sys.exit(0)
