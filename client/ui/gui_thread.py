# -*- coding:utf8 -*-
# @TIME     : 2020/7/31 15:28
# @Author   : Hao Su
# @File     : gui_thread.py


'''
需要用到的多线程
相机读取函数
'''

import cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import time


class Videothread(QThread, QObject):
    videothread_signal = pyqtSignal(dict)
    camera_error_signal = pyqtSignal()
    # plotROI_signl = pyqtSignal(dict)

    def __init__(self):
        '''
        :param label: 构造函数初始化相机的序号
        '''
        super(Videothread, self).__init__()
        self.cap = None
        self.flag = 1       # 用于终止线程的标志位


    def run(self):
        while 1:
            if self.flag:
                try:
                    _, self.img = self.cap.read()
                    if self.img is not None:
                        img_dict = {"img": self.img}
                        self.videothread_signal.emit(img_dict)
                    else:
                        pass
                        # self.flag = 0
                        # self.camera_error_signal.emit()
                except:
                    pass
            else:
                return


class DetecThread(QThread, QObject):
    detecthread_signal = pyqtSignal(dict)
    warning_signal = pyqtSignal(int)
    camera_error_signal = pyqtSignal()
    grayImage_signal = pyqtSignal(dict)

    def __init__(self):
        super(DetecThread, self).__init__()
        self.cap = None
        self.img = None
        self.ROILoc = 0
        self.flag = 1       # 标志位：用于从外部将线程停下来
        self.flag_detect = 1
        self.flag_detect_auto = 0       # 表示位用于表示是否进行自动检测，0表示否
        self.patch_Rect = (0, 0, 0, 0)


    def getROILocation(self, ROILoc):
        self.ROILoc = ROILoc


    def cutROIpicture(self, img):
        if self.ROILoc:     # 如果人为制定了ROI
            center = self.ROILoc["center"]
            r = self.ROILoc["r"]
            a = int(center[1] - r);
            b = int(center[1] + r + 1)
            c = int(center[0] - r);
            d = int(center[0] + r + 1)  # 注意需要转换为整型
            if a > 0 and c > 0 and b < img.shape[0] and d < img.shape[1]:  # 检查ROI区域是否超出图片范围
                # mask = np.zeros_like(img)
                # mask = cv2.circle(mask, (int(center[0]), int(center[1])), int(r), (1, 1, 1), -1)
                # ROIImage = img * mask
                # ROIImage = ROIImage[a:b, c:d, :]
                ROIImage = img[a:b, c:d, :]
                return ROIImage
            else:
                return 0
        else:
            pass        #   否则自动寻找ROI


    def run(self):
        while 1:
            if self.flag:                                   # 子线程循环标志
                try:
                    if self.flag_detect:                    # 处于视屏检测模式
                        _, img = self.cap.read()
                    else:                                   # 处于usb文件检测模式
                        img = self.img
                    if img is not None:                     # 是否正确读取到图像
                        self.ROIImage = self.cutROIpicture(img)
                        if not isinstance(self.ROIImage, int):          # ROI是否超出范围
                            # results = Detect(img=self.ROIImage)  # 菌落计数检测算法
                            img_dict = {"img": self.ROIImage}
                            self.detecthread_signal.emit(img_dict)
                        else:                                       # 检查ROI区域是否超出图片范围
                            self.warning_signal.emit(0)
                            return
                    else:
                        self.flag = 0
                        self.camera_error_signal.emit()
                except:
                    return
            else:
                return
            

class StaticImage_DetecThread(QThread):
    '''这个线程用于点击暂停以后进行静态检测
    这里我们认为在初始情况下shezhiwanROI区域以后，无法再修改ROI区域
    因此在这个线程的构造函数里，我们只传入之前连续检测时得到的ROI区域'''
    staticdetecthread_signal_img = pyqtSignal(dict)
    staticdetecthread_signal_target = pyqtSignal(dict)
    # grayImage_signal = pyqtSignal(dict)

    def __init__(self):
        super(StaticImage_DetecThread, self).__init__()
        self.ROIImage = 0
        self.ROILoc = 0
        self.flag = 1
        self.flag_detect_auto = 0
        self.patch_Rect = (0, 0, 0, 0)


    def getROIImage(self, img):
        self.ROIImage = img


    def run(self):
        resultImage, targets = self.ROIImage, []
        img_dict = {"img": resultImage}
        targets_dict = {"targets": targets}
        self.staticdetecthread_signal_img.emit(img_dict)
        # self.staticdetecthread_signal_target.emit(targets_dict)

