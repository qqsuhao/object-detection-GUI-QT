# -*- coding:utf8 -*-
# @TIME     : 2020/7/31 17:33
# @Author   : Hao Su
# @File     : pain_ROI.py

'''
绘制图形的类
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np


class Painting(QLabel):
    Painting_num_signal = pyqtSignal(int)
    plotpatch_signal = pyqtSignal()

    def __init__(self, parent=None):
        # 这一行需要parent，否则画笔找不到父类对象， 结果就是程序不报错，但是看不到绘制结果
        super(Painting, self).__init__(parent)
        self.pencolor = Qt.blue                 # 画笔颜色
        self.penwidth = 4                       # 画笔宽度
        self.ROI_rect = (0, 0, 0, 0)            # 用于绘图的位置参数
        self.board = QPixmap()                  # 创建画布
        self.board.fill(Qt.transparent)         # 透明画布
        self.painter = QPainter()               # 创建画笔
        self.flag_ROI = 1                       # 标志位：是否处于绘制ROI阶段
        self.flag_match = 0                     # 标志位：模板选取阶段
        self.flag_right = 0                    # 标志位：是否选择了用鼠标左键代替鼠标右键的功能
        # self.flag_right需要对鼠标点击，移动，释放这三个时间函数进行限制
        '''绘图主要用于两种情况，一种是绘制ROI，另一种是标记菌落。绘制ROI只能绘制一个圆'''
        self.init_draw_targets()
        self.pencolor_origin = Qt.red
        self.penwidth_origin = 4
        self.num = 0                        # 记录菌落的数量
        self.Leftbutton = False
        '''
        用于判断是否为鼠标左键移动，如果直接在重载鼠标移动函数中加入Qt.LeftButton, 
        会导致看不到移动过程中的连续绘图效果
        '''


    def init_Pixmap(self, label_size):
        '''初始化画布'''
        self.board = QPixmap(label_size)        # 初始化画布尺寸
        self.board.fill(Qt.transparent)         # 初始化画布背景填充，填充为透明


    def init_draw_targets(self):
        self.targets = np.array([[0,0,0,0,0]])
        self.num = 0                                # 重置为0


    def setcolor(self, c):
        '''设置画笔颜色'''
        self.pencolor = c
        self.update()


    def setwidth(self, w):
        '''设置画笔宽度'''
        self.penwidth = w
        self.update()


    def setscale(self, scale):
        '''从原图像得到的目标位置需要进行缩放才能正确显示'''
        self.scale = scale


    def paintEvent(self, event):
        '''这个函数会不停地运行
        鼠标事件会不停修改ROI_rec的值，从而使得拖动鼠标的过程中可以看到我们绘制的圆在不停变化
        但是再次点击鼠标以后，ROI_rec会变成0，导致之前绘制的圆消失。
        解决的方法是单独设置一个Qpixmap,每次松开鼠标以后，把图形绘制到Qpixmap上保存
        同时paintEvent()每次都要执行self.painter.drawPixmap(0, 0, self.board)
        '''
        super().paintEvent(event)       # 没有这一行代码，图像无法显示，只能绘图
        self.painter.begin(self)                                 # 开始绘图，没有这一句无法显示图像
        # 注意begin()里面需要使用self
        self.painter.setPen(QPen(self.pencolor, self.penwidth))  # 设置画笔
        if self.flag_match:
            self.painter.drawRect(*self.ROI_rect)
        else:
            self.painter.drawRect(*self.ROI_rect)                 # 绘制圆形
        if not self.flag_ROI:                                    # 如果出于ROI绘制阶段，限制图上只出现一个圆
            self.painter.drawPixmap(0, 0, self.board)            # 绘制QPixmap上的内容
        self.painter.end()



    def mousePressEvent(self, event):  # 重写三个事件处理
        if event.button() == Qt.LeftButton and self.flag_right == 0:
            self.ROI_rect = (event.x(), event.y(), 0, 0)
            self.Leftbutton = True
            self.update()
        elif (event.button() == Qt.LeftButton and self.flag_right == 1) or event.button() == Qt.RightButton:
            if not self.flag_ROI:
                index = self.FindNearestTarget(event.x(), event.y())
                if index > -1:
                    selecttarget = self.targets[index, :]
                    pp = QPainter(self.board)  # 每次绘制结束时保存所绘制的圆
                    # self.board.
                    pp.begin(self)
                    pp.setPen(QPen(Qt.black, selecttarget[4]))
                    pp.drawRect(*selecttarget[0:4])
                    pp.end()
                    self.update()
                    self.num -= 1           # 非绘制ROI情况下，点击鼠标左键减一
                    self.targets = np.delete(self.targets, index, axis=0)
                    self.Painting_num_signal.emit(self.num)


    def mouseMoveEvent(self, event):
        if self.Leftbutton and self.flag_right == 0:
        # if event.button() == Qt.LeftButton:
            start_x, start_y = self.ROI_rect[0:2]
            edge = min(event.x() - start_x, event.y() - start_y)    # 为了画成标准圆而不是椭圆
            self.ROI_rect = (start_x, start_y, edge, edge)
            self.update()



    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.flag_right == 0:
            start_x, start_y = self.ROI_rect[0:2]
            edge = min(event.x() - start_x, event.y() - start_y)    # 为了画成标准圆而不是椭圆
            self.ROI_rect = (start_x, start_y, edge, edge)
            self.Leftbutton = False
            self.plotpatch_signal.emit()
            self.update()
            if not self.flag_ROI:
                rect = (0, 0, 0, 0)
                if edge > 0:            # 防止鼠标只是点击了一下，并没有移动
                    rect = self.ROI_rect
                    tmp = np.c_[np.array(list(self.ROI_rect)).reshape(1, 4), np.array([[self.penwidth]])]
                    self.targets = np.r_[self.targets, tmp]
                    self.num += 1               # 非绘制ROI情况下，点击鼠标左加一
                    self.Painting_num_signal.emit(self.num)
                elif edge < 0:          # 防止鼠标沿左上角移动
                    rect = (self.ROI_rect[0]+self.ROI_rect[2], self.ROI_rect[1]+self.ROI_rect[3],
                            -1*self.ROI_rect[2], -1*self.ROI_rect[3])
                    tmp = np.c_[np.array(list(rect)).reshape(1, 4), np.array([[self.penwidth]])]
                    self.targets = np.r_[self.targets, tmp]
                    self.num += 1               # 非绘制ROI情况下，点击鼠标左加一
                    self.Painting_num_signal.emit(self.num)
                pp = QPainter(self.board)                               # 每次绘制结束时保存所绘制的圆
                pp.setPen(QPen(self.pencolor, self.penwidth))
                pp.drawRect(*rect)


    def getROI_location(self):  # 获取ROI区域的位置
        return self.ROI_rect


    def plot_targets(self, targets):
        '''绘制检测以后得到的目标
        注意这里需要对位置参数进行缩放'''
        if targets.size > 0:            # 以防止算法返回的是一个空的数组
            self.targets = targets.copy()
            self.flag_ROI = 0
            self.num = self.targets.shape[0]            # 目标数量
            pp = QPainter(self.board)  # 每次绘制结束时保存所绘制的圆
            # pp.begin()
            pp.setPen(QPen(self.pencolor, self.penwidth))
            for i in range(self.targets.shape[0]):
                self.targets[i, 4] = self.penwidth              # 记录绘制每个目标的线宽
                pp.drawRect(*self.targets[i, 0:4])
            # pp.end()
            self.Painting_num_signal.emit(self.targets.shape[0])
            self.num = self.targets.shape[0]


    def FindNearestTarget(self, x, y):
        '''根据坐标位置判断最近的一个目标'''
        if self.targets.size > 0:
            diff_left = self.targets[:, 0:2] < np.array([x, y])
            diff_right = (self.targets[:, 0:2] + self.targets[:, 2:4]) > np.array([x, y])
            diff = np.c_[diff_left, diff_right]
            diff = diff ^ [True, True, True, True]
            tmp = diff[:,0] | diff[:,1] | diff[:,2] | diff[:,3]
            order = np.where(tmp == False)[0]
            if order.size > 0:
                return order[0]
            else:
                return -1                 # 如果没有找到，就返回空
        else:
            return -1     # 如果targets是空的，就返回空




