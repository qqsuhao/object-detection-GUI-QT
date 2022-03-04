# -*- coding:utf8 -*-
# @TIME     : 2020/7/31 11:39
# @Author   : Hao Su
# @File     : main.py

'''
程序运行的主函数
'''

from client.ui.Mainwindow import *
from PyQt5.QtWidgets import QWidget, QApplication
import sys
from client.ui.print_log import *
import os, sys


if __name__ == '__main__':
    # 初始化日志记录
    os.chdir(sys.path[0])
    try:
        os.remove('LOG.log')
        os.remove('ERROR.log')
    except:
        pass
    sys.stdout = Logger('LOG.log', sys.stdout)  # 控制台输出日志
    sys.stderr = Logger('ERROR.log', sys.stderr)  # 错误输出日志
    App = QApplication(sys.argv)
    window = Mainwindow()
    window.setWindowFlags(QtCore.Qt.Window)
    window.showFullScreen()
    # window.show()
    sys.exit(App.exec_())
