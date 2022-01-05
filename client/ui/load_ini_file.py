# -*- coding:utf8 -*-
# @TIME     : 2020/8/8 14:27
# @Author   : Hao Su
# @File     : load_ini_file.py

'''
b保存和加载init.txt文件，用于
'''


def save_init_file(dict_params, path="init.txt"):
    if isinstance(dict_params, dict):
        file = open(path, 'w')  # 先创建并打开一个文本文件
        # 遍历字典的元素，将每项元素的key和value分拆组成字符串，注意添加分隔符和换行符
        for k, v in dict_params.items():
            file.write(str(k) + ' ' + str(v) + '\n')
        file.close()  # 注意关闭文件


def read_init_file(path="init.txt"):
    dict_temp = {}
    file = open(path, 'r') # 打开文本文件
    # 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
    for line in file.readlines():
        line = line.strip()
        k = line.split(' ')[0]
        v = line.split(' ')[1]
        dict_temp[k] = v
    file.close()        # 依旧是关闭文件
    return dict_temp


def params_legal_ornot(dict_params):
    ''' 检查字典参数是否合法
    :return: 
    '''
    key = ['th', 'th2', 'th4', 'binthreshold']
    for k, v in dict_params.items():
        if not k in key:
            return False
    return True
