# -*- coding:utf8 -*-
# @TIME     : 2020/8/2 17:27
# @Author   : Hao Su
# @File     : Mainwindow.py
'''
继承图形界面设计文件
'''

import cv2
from client.ui.gui import *
from client.ui.gui_thread import *
from client.ui.paint_ROI import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
import platform
from client.ui.load_ini_file import *
from client.ui.read_usb import *
from client.ui.chart import *
from client.ui.utils import *
import os
import psutil
from client.ui.httpclient import *


def Sleep(msec):
    dieTime = QTime.currentTime().addMSecs(msec)
    while QTime.currentTime() < dieTime:
        QCoreApplication.processEvents(QEventLoop.AllEvents, 100)


class Mainwindow(QWidget, Ui_counting_Form):    # 需要继承设计文件中的类和QWidget
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        # 界面初始化
        self.UI_init()
        # 标志位初始化
        self.system = platform.system()     # 检测系统是windows还是linux
        self.camera_label = 210
        if self.system == "Windows":
            self.camera_label = 700        # 相机
        self.flag_cap = 0           # 标志位：是否有相机
        self.flag_usb = 0           # 标志位：是否插入USB
        self.flag_play = 1          # 标记是进行播放还是停止
        self.flag_ROI = 0           # 标记是否设置了ROI区域
        self.flag_detect = 1        # 标志位：当前是使用相机检测还是使用文件批量检测
        self.flag_first = 0         # 第一次点击播放需要检测ROI是否合理
        self.ip = None                # 局域网ip地址
        self.cal_time = 0           # 服务器计算所需时间
        '''
        这里着重说明self.flag_first的作用：由于第一次设置完ROI以后，
               首次执行play需要关闭普通线程以及其他的相关操作，这个时候self.flag_first派上用场
               这之后由于ROI相关的ROILOC被重置为0，因此self.ROI会变成0，会导致play_and_pause()
            无法正常运行，为此需要使用self.flag_first'''
        # 用于后边记录原始图像的大小和填充后的大小
        self.origin_width = 0;  self.origin_heigh = 0
        self.scaled_width = 0;  self.scaled_heigh = 0
        self.cap_width = 0;  self.cap_heigh = 0             # 相机尺寸
        # usb文件检测线程初始化
        # self.usb_thread_init()
        # 线程初始化
        self.thread_init()
        # 画笔初始化
        self.painter_init()
        # 信号和槽函数连接初始化
        self.signalslot_init()
        # 定时器初始化
        self.timer_init()
        # 相机和USB监视
        self.monitor_camera()       # 检测相机
        self.monitor_usb()          # 检测USB
        # 表格初始化
        self.chart1, self.chart2, self.chart3 = Chart(), Chart(), Chart()
        self.chart_init()



    def __del__(self):          # 2020.11.12 新添加析构函数
        self.videothread.flag = 0
        self.videothread.wait()
        self.videothread.quit()
        self.timer_monitor_usb.stop()
        self.timer_monitor_camera.stop()
        self.chart_thread1.stop()
        self.mythread1.isexit = False
        self.chart_thread1.wait()
        self.chart_thread1.quit()
        self.chart_thread2.stop()
        self.mythread2.isexit = False
        self.chart_thread2.wait()
        self.chart_thread2.quit()
        self.chart_thread3.stop()
        self.mythread3.isexit = False
        self.chart_thread3.wait()
        self.chart_thread3.quit()




    def UI_init(self):
        '''部分界面设置初始化'''
        self.pushButton_color.setPalette(QPalette(Qt.blue))  # 在frame中填充画笔颜色
        # 设置两个icon，用于后期usb图标的切换
        self.icon_usb_on = QtGui.QIcon()
        self.icon_usb_on.addPixmap(QtGui.QPixmap(":/pics/pics/usb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_usb_off = QtGui.QIcon()
        self.icon_usb_off.addPixmap(QtGui.QPixmap(":/pics/pics/usb_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # 设置两个icon，用于后期play和pause图标的切换
        self.icon_pause = QtGui.QIcon()
        self.icon_pause.addPixmap(QtGui.QPixmap(":/pics/pics/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.icon_play = QtGui.QIcon()
        self.icon_play.addPixmap(QtGui.QPixmap(":/pics/pics/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)




    def thread_init(self):
        # 动态检测线程
        self.detecthread = DetecThread()
        self.detecthread.detecthread_signal.connect(self.play_video)
        self.detecthread.camera_error_signal.connect(lambda: self.Warning_notice(1))
        # 普通视屏播放线程
        self.videothread = Videothread()
        self.videothread.videothread_signal.connect(self.play_video)
        self.videothread.camera_error_signal.connect(lambda: self.Warning_notice(1))
        # self.videothread.plotROI_signal.connect(self.auto_select_ROI)
        self.videothread.start()
        # 静态图片检测线程
        self.staticdetecthread = StaticImage_DetecThread()
        self.staticdetecthread.staticdetecthread_signal_img.connect(self.play_video)
        # self.staticdetecthread.staticdetecthread_signal_target.connect(self.plot_targets)
        # 绘制表格线程
        # self.chart_thread1 = WorkThread(t=1)
        # self.chart_thread1._signal_updateUI.connect(self.draw_qchart1)
        # self.chart_thread1.start()
        # self.chart_thread2 = WorkThread(t=0.2)
        # self.chart_thread2._signal_updateUI.connect(self.draw_qchart2)
        # self.chart_thread2.start()
        # self.chart_thread3 = WorkThread(t=0.2)
        # self.chart_thread3._signal_updateUI.connect(self.draw_qchart3)
        # self.chart_thread3.start()
        ## http ping
        self.ping_thread = PingThread(ip=self.ip, sleep_time=0.5)
        self.ping_thread.ping_signal.connect(self.draw_qchart1)
        self.http_client = HttpClient(self.ip)
        self.http_client.http_signal.connect(self.draw_qchart2)
        self.http_client.conf_signal.connect(self.draw_qchart3)
        self.http_client.loc_signal.connect(self.plot_targets)


    def painter_init(self):
        # 画笔
        self.label_paint = Painting(self.label_12)      # 父对象指定为label_12,可以使得只在label_12中绘图
        # self.label_paint.setCursor(Qt.CrossCursor)
        self.paint_width = self.label_12.geometry().width()
        self.paint_heigh = self.label_12.geometry().height()
        self.label_paint.setGeometry(QRect(0, 0, self.paint_width, self.paint_heigh))  # 在label_12中指定其相对于label_12的位置


    def signalslot_init(self):
        # 更改颜色按钮
        self.pushButton_color.clicked.connect(self.pencolor_choose)
        # 保存按钮槽函数
        self.pushButton_save.clicked.connect(self.saveLabelImage)
        # usb按钮，开启文件检测模式槽函数
        self.pushButton_usb.clicked.connect(self.process_usb)
        # 文件检测模式下切换文件槽函数
        self.pushButton_usb_left.clicked.connect(lambda: self.next_usb_img(0))
        self.pushButton_usb_right.clicked.connect(lambda: self.next_usb_img(1))
        # 关闭程序按钮，要区分是什么系统
        if self.system == "Windows":
            self.pushButton_power.clicked.connect(self.__del__)
            self.pushButton_power.clicked.connect(QCoreApplication.quit)
        else:
            self.pushButton_power.clicked.connect(self.power)
        # 绘制patch
        self.label_paint.plotpatch_signal.connect(self.plot_patch)
        # 更新软件槽函数
        self.pushButton_update.clicked.connect(self.update_software)
        # 连接局域网
        self.pushButton_http.clicked.connect(self.connect_http)



    def timer_init(self):
        if self.system == "Linux":
            self.timer_temp = QTimer()
            self.timer_temp.timeout.connect(self.get_temp)
            self.timer_temp.start(2000)



    def chart_init(self):
        self.graphicsView.setChart(self.chart1)
        self.graphicsView_2.setChart(self.chart2)
        self.graphicsView_3.setChart(self.chart3)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.graphicsView_2.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.graphicsView_3.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        ft = QFont()
        ft.setPixelSize(12)
        self.chart1.setTitleFont(ft)
        self.chart1.axisY.setTitleText("Ping(ms)")
        self.chart2.setTitleFont(ft)
        self.chart2.axisY.setTitleText("FPS(ms)")
        self.chart3.setTitleFont(ft)
        self.chart3.axisY.setTitleText("Conf")


    def params_save(self, dict_params):
        save_init_file(dict_params)


    def monitor_camera(self):
        ''' 检测相机是否存在，若不存在，则设置定时器不停地检测 '''
        cap = cv2.VideoCapture(self.camera_label)
        if not cap.isOpened():
            print("Do Not Detect Camera.")
            self.label_12.setPixmap(QtGui.QPixmap(":/pics/pics/prohibition.png"))
            self.label_12.setScaledContents(True)
            self.flag_cap = 0
            self.timer_monitor_camera = QTimer()
            self.timer_monitor_camera.timeout.connect(self.open_camera)
            self.timer_monitor_camera.start(2000)
        else:
            print("Detect Camera.")
            self.cap = cap
            self.videothread.cap = cap
            self.detecthread.cap = cap
            self.flag_cap = 1
            _, img = self.cap.read()
            self.cap_heigh, self.cap_width = img.shape[0], img.shape[1]


    def open_camera(self):
        '''检测相机定时器的槽函数'''
        cap = cv2.VideoCapture(self.camera_label)
        self.flag_cap = cap.isOpened()
        if self.flag_cap:
            self.timer_monitor_camera.stop()         # 检测到相机，关闭定时器
            # self.cap = cap
            self.videothread.cap = cap
            self.detecthread.cap = cap
            _, img = self.cap.read()
            self.cap_heigh, self.cap_width = img.shape[0], img.shape[1]
            reply = QMessageBox.information(self,  # 使用infomation信息框
                                            "Monitor Camera",
                                            "We Detect a Camera, Whether Use It?",
                                            QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.thread_init()
                self.clear_ROI()        # stop按钮的槽函数


    def monitor_usb(self):
        '''监控usb设备的状态'''
        self.usb_monitor = USB()
        self.timer_monitor_usb = QTimer()
        self.timer_monitor_usb.timeout.connect(self.open_usb)
        self.timer_monitor_usb.start(2000)


    def open_usb(self):
        self.flag_usb = self.usb_monitor.check_usb()
        if self.flag_usb:
            self.pushButton_usb.setIcon(self.icon_usb_on)
        else:
            self.usb_monitor.params_init()
            self.pushButton_usb.setIcon(self.icon_usb_off)


    def pencolor_choose(self):
        '''
        :return: 修改画笔颜色的槽函数
        '''
        color = QColorDialog.getColor(Qt.blue)          # 弹出颜色选择框
        self.pushButton_color.setPalette(QPalette(color))
        self.label_paint.setcolor(color)                       # 默认画笔颜色


    def penwidth_choose(self, w):
        '''
        :return: 修改画笔颜色的槽函数
        '''
        self.label_paint.setwidth(w)                   # 默认画笔颜色


    def play_video(self, img_dict):
        '''
        将得到的img转换为QImage格式，然后显示在graphview上
        :param img_dict:这里由于信号只能发送字典，而这个函数是被当做槽函数来使用的
        :return:
        '''
        img = img_dict['img']
        # img = np.transpose(img, [1, 0, 2])
        ##
        if self.detecthread.isRunning():
            if self.http_client.qmut.tryLock():
                self.http_client.img = img
                self.http_client.qmut.unlock()
        ##
        y, x, dim = img.shape  # 获取图像大小
        self.origin_width = x
        self.origin_heigh = y
        if dim == 4:
            frame = QImage(img, x, y, x * 4, QImage.Format_RGB32)
        elif dim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        elif dim == 1:
            frame = QImage(img, x, y, x * 1, QImage.Format_Grayscale8)
        else:
            raise Exception("image channels must be 1,3,4")
        frame_scaled = frame.scaled(QSize(self.paint_width, self.paint_heigh), Qt.KeepAspectRatio)
        pix = QPixmap.fromImage(frame_scaled)
        self.scaled_width = frame_scaled.width()
        self.scaled_heigh = frame_scaled.height()   # 记录填充后的图片大小
        self.update()
        self.label_paint.setscale(self.origin_width / self.scaled_width)
        self.label_paint.setPixmap(pix)
        self.label_paint.setAlignment(Qt.AlignCenter)
        self.label_paint.update()

        # item = QGraphicsPixmapItem(pix)  # 创建像素图元
        # scene = QGraphicsScene()  # 创建场景
        # scene.clear()
        # scene.addItem(item)
        # self.graphicsView.setScene(scene)



    def play_and_pause(self):
        ROI_loc = self.label_paint.getROI_location()            # 获取ROI区域的相对于当前播放内容的位置
        if ROI_loc[2] > 0:                                          # 如果已设置ROI，更新标记位
            self.flag_ROI = 1
        if self.flag_ROI or self.flag_first:                                       # 检测是否划定了ROI区域
            if self.flag_play:                                  # 进行动态检测
                ROILoc = self.getROILocInImage()                # 从原图截取ROI区域并进行播放
                if self.ROI_beyond_scope_ornot(ROILoc) or self.flag_first: # 如果ROI没有问题
                    if not self.flag_first:      # 表示画好ROI后的第一次点击运行
                        self.detecthread.getROILocation(ROILoc)
                    if self.videothread.isRunning():            # 防止后续按键的时候导致重复选取ROI
                        # 通过普通播放线程是否运行来确定当前绘图是否是ROI绘图
                        self.videothread.flag = 0               # 修改线程运行标志位
                        self.videothread.quit()                 # 停止播放线程，退出线程
                        self.videothread.wait()
                        # self.detecthread.getROILocation(ROILoc)
                    if self.staticdetecthread.isRunning():
                        self.staticdetecthread.flag = 0
                        self.staticdetecthread.quit()
                        self.staticdetecthread.wait()
                    self.label_paint.init_Pixmap(self.label_12.size())      # 清空画布
                    self.label_paint.init_draw_targets()                    # 清空缓存
                    self.label_paint.ROI_rect = (0, 0, 0, 0)    # 不再显示ROI圆形
                    self.label_paint.flag_ROI = 1               # 不允许画布显示多个图像
                    self.label_paint.flag_match = 1             # 模板选取阶段
                    self.detecthread.patch_Rect = (0, 0, 0, 0)
                    self.staticdetecthread.patch_Rect = (0, 0, 0, 0)
                    self.detecthread.flag = 1                   # 修改检测线程标志位
                    self.detecthread.img = self.usb_monitor.img
                    self.detecthread.start()                    # 开始检测

                    self.http_client.img = None
                    self.http_client.flag = 1
                    self.http_client.start()

                    self.pushButton_start.setIcon(self.icon_pause)
                    self.flag_play = 0                          # 标记反转
                    self.flag_first = 1
                    self.update()
                else:
                    self.flag_ROI = 0
                    self.Warning_notice(0)                      # 弹出警告框
            else:               # 截取静止状态
                self.label_paint.flag_ROI = 0           # 允许画布显示多个图像
                self.label_paint.flag_match = 0           # 结束模板选择阶段
                self.label_paint.ROI_rect = (0, 0, 0, 0)
                self.detecthread.flag = 0  # 停止播放
                self.detecthread.quit()
                self.detecthread.wait()

                self.http_client.flag = 0
                self.http_client.quit()
                self.http_client.wait()

                self.staticdetecthread.getROIImage(self.detecthread.ROIImage)  # 对当前图片进行处理
                self.staticdetecthread.start()
                self.pushButton_start.setIcon(self.icon_play)
                self.flag_play = 1          # 标记反转

        else:                   # 如果没有划定ROI区域，弹出警告框
            QMessageBox.warning(self, "Warning", "Please set ROI!")


    def getROILocInImage(self):
        '''获取ROI相对于label中图片的位置，并进行转换，得到对于原始尺寸的图片，对应ROI的位置
        '''
        ROI_loc = self.label_paint.getROI_location()
        r = int(ROI_loc[2] / 2)
        center = [int(ROI_loc[0]) + r, int(ROI_loc[1]) + r]
        # if self.scaled_width > self.scaled_heigh:
        #     center = [center[0], center[1] - (self.label_paint.height()/2 - self.scaled_heigh/2)]
        # else:
        #     pass
        # scale_coe = self.origin_width / self.scaled_width
        # center, r = [center[0]*scale_coe, center[1]*scale_coe], r * scale_coe
        scale_coe = self.origin_width / self.scaled_width
        r = r*scale_coe
        center[0], center[1] = self.FromLabelToImage(center[0], center[1])
        return {"center": center, "r": r}


    def ROI_beyond_scope_ornot(self, ROILoc):
        '''根据照相机的画面大小判断ROI区域是否超出范围
        :param ROILoc: 字典
        :return:
        '''
        if ROILoc:     # 如果人为制定了ROI
            center = ROILoc["center"]
            r = ROILoc["r"]
            a = int(center[1] - r);
            b = int(center[1] + r + 1)
            c = int(center[0] - r);
            d = int(center[0] + r + 1)  # 注意需要转换为整型
            if a > 0 and c > 0 and b < self.origin_heigh and d < self.origin_width:
                return True
            else:
                return False
        else:
            return False


    def ROI_beyond_scope_ornot_USB(self, ROILoc):
        '''根据照相机的画面大小判断ROI区域是否超出范围
        :param ROILoc: 字典
        :return:
        '''
        if ROILoc:     # 如果人为制定了ROI
            center = ROILoc["center"]
            r = ROILoc["r"]
            a = int(center[1] - r);
            b = int(center[1] + r + 1)
            c = int(center[0] - r);
            d = int(center[0] + r + 1)  # 注意需要转换为整型
            if a > 0 and c > 0 and b < self.usb_monitor.img.shape[0] \
                    and d < self.usb_monitor.img.shape[1]:
                return True
            else:
                return False
        else:
            return False


    def showEvent(self, a0: QtGui.QShowEvent):
        '''防止全屏显示导致图片尺寸不正确'''
        self.resizeEvent(a0)


    def resizeEvent(self, a0: QtGui.QResizeEvent):
        '''
        窗口大小改变以后label_12的大小也会改变，因此需要重写该事件。
        改变大小以后更新label_12的宽和高，同时更新画布的大小
        :param a0:
        :return:
        '''
        self.paint_width = self.label_12.geometry().width()
        self.paint_heigh = self.label_12.geometry().height()
        self.label_paint.init_Pixmap(self.label_12.size())
        self.label_paint.setGeometry(QRect(0, 0, self.paint_width, self.paint_heigh))  # 在label_12中指定其相对于label_12的位置
        self.label_paint.flag_ROI = 1
        self.update()



    def Warning_notice(self, param):
        if param == 0:      # 处理ROI超出范围的问题
            self.label_paint.ROI_rect = (0, 0, 0, 0)
            self.flag_ROI = 0
            self.flag_play = 1
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/pics/pics/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_start.setIcon(icon)
            QMessageBox.warning(self, "Warning", "The Area of ROI is Beyond Scope.")
            print("[Warning]: The Area of ROI is Beyond Scope.")
        elif param == 1:
            reply = QMessageBox.warning(self, "Warning", "Camera is Off Line. Please Check Your Camera and Reboot.")
            if reply == QMessageBox.Ok:
                # QCoreApplication.quit()
                os.system("reboot")


    def clear_ROI(self):
        '''stop按钮的槽函数'''
        if self.flag_cap == 1:
            self.flag_detect = 1        # 切换为视频检测模式
            self.flag_ROI = 0                               # ROI标志位清零
            self.label_paint.ROI_rect = (0, 0, 0, 0)        # 绘图清零
            self.label_paint.flag_ROI = 1                   # 处于绘制ROI阶段
            self.label_paint.flag_match = 0  # 结束模板选择阶段
            self.update()
            self.flag_play = 1
            self.flag_first = 0
            self.label_paint.init_Pixmap(self.label_12.size())  # 清空画布
            self.label_paint.init_draw_targets()                # 清空缓存
            self.pushButton_start.setIcon(self.icon_play)
            if self.detecthread.isRunning():            # 如果处于检测线程，退出检测线程
                self.detecthread.flag = 0
                self.detecthread.quit()
                self.detecthread.wait()

                self.http_client.flag = 0
                self.http_client.quit()
                self.http_client.wait()

                self.detecthread.flag_detect = 1
            if self.staticdetecthread.isRunning():      # 如果处于检测线程，退出检测线程
                self.staticdetecthread.flag = 0
                self.staticdetecthread.quit()
                self.staticdetecthread.wait()
            if self.flag_cap and (not self.videothread.isRunning()):                           # 如果连接了相机
                self.videothread.flag = 1
                self.videothread.start()                    # 开始播放原来的普通线程
            else:
                self.label_paint.setPixmap(QPixmap(" "))
            Sleep(10)
            self.label_paint.init_Pixmap(self.label_12.size())  # 清空画布



    def FromImageToLabel(self, X, Y):
        '''从图片的坐标位置映射到label的坐标位置'''
        scale_coe = self.origin_width / self.scaled_width
        X, Y = X / scale_coe, Y / scale_coe
        # if self.scaled_width >= self.scaled_heigh:
        Y = Y + (self.label_12.height()/2 - self.scaled_heigh/2)
        X = X + (self.label_12.width()/2 - self.scaled_width/2)
        return int(X), int(Y)


    def FromLabelToImage(self, X, Y):
        '''从label的坐标位置映射到图片的坐标位置'''
        Y = Y - (self.label_12.height()/2 - self.scaled_heigh/2)
        X = X - (self.label_12.width()/2 - self.scaled_width/2)
        scale_coe = self.origin_width / self.scaled_width
        X, Y = X*scale_coe, Y*scale_coe
        return int(X), int(Y)



    def plot_targets(self, targets_dict):
        '''静态图片检测线程的槽函数，用于绘制检测结果
        targets_cir：
        targets
        '''
        self.label_paint.init_Pixmap(self.label_12.size())
        targets_cir_tmp = targets_dict["targets"]
        targets_cir = targets_cir_tmp * self.origin_width
        scale_coe = self.origin_width / self.scaled_width       # 缩放倍数
        if targets_cir.size > 0:                # 如果矩阵非空
            targets = np.zeros((targets_cir.shape[0], 5))       # 将targets_cir转换为targets
            for i in range(targets_cir.shape[0]):
                w, h = targets_cir[i, 2], targets_cir[i, 3]
                x, y = targets_cir[i, 0], targets_cir[i, 1]
                a, b = self.FromImageToLabel(x, y)            # 计算图片中的位置对应到label中的位置
                targets[i, 2], targets[i, 3] = int(w / scale_coe), int(h / scale_coe)
                targets[i, 0], targets[i, 1] = a, b
            self.label_paint.plot_targets(targets)
        else:
            self.label_paint.plot_targets(targets_cir)      # 传递一个空矩阵
            # self.label_paint.plot_targets在运行前会再次检测矩阵是否为空
        self.update()           # 刷新绘图



    def QImageToMat(self, qimg):
        '''将QImage转换为Mat类型'''
        ptr = qimg.constBits()
        ptr.setsize(qimg.byteCount())
        img = np.array(ptr).reshape(qimg.height(), qimg.width(), 4) # 注意这里要使用4
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img


    def saveLabelImage(self):
        '''保存label中的图像'''
        if self.flag_cap == 1:
            # 打开保存文件的窗口
            if self.flag_usb:
                path = self.usb_monitor.usb_path
                savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', path, '*.png')
            else:
                savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', './', '*.png')
            if savePath[0] == "":
                print("Save cancel")
                return
            qimg = self.label_paint.pixmap().toImage()
            qimg_1 = self.label_paint.board.toImage()
            img = self.QImageToMat(qimg)
            img_1 = self.QImageToMat(qimg_1)
            cut_area_h = int((img_1.shape[0] - img.shape[0]) / 2)
            cut_area_w = int((img_1.shape[1] - img.shape[1]) / 2)
            # img = cv2.addWeighted(img, 1, img_1[cut_area:cut_area+img.shape[0], 0:img.shape[0], :], 2, 0)
            # 以下操作是为了将图片和绘制的圆两个图层合并到一起
            img_1 = img_1[cut_area_h:cut_area_h+img.shape[0], cut_area_w:cut_area_w+img.shape[1], :]
            gray = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 2, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            img_bg = cv2.bitwise_and(img, img, mask=mask_inv)
            img_1_fg = cv2.bitwise_and(img_1, img_1, mask=mask)
            img = cv2.add(img_bg, img_1_fg)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # cv2.putText(img, self.label_14.text(), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
            # 由于两种系统下，输入文件路径稍有区别，所以需要单独进行设置
            if self.system == "Windows":
                path = savePath[0]
            else:
                path = savePath[0] + ".png"
            cv2.imwrite(path, img)

            ## 如果文件以template命名，将其作为模板图像发送至服务器
            img_name = os.path.split(path)[-1].split(".")[0]
            if img_name == "template":
                self.http_client.transfer_to_server(img)


    def process_usb(self):
        '''usb按键的槽函数'''
        if self.flag_usb:       # r如果已经插入了usb，则进入文件检测模式
            self.label_paint.init_Pixmap(self.label_12.size())      # 清空画布
            self.label_paint.init_draw_targets()                    # 清空缓存
            self.label_paint.ROI_rect = (0, 0, 0, 0)                # 不再显示ROI圆形
            self.label_paint.flag_ROI = 1                           # 不允许画布显示多个图像
            self.label_paint.flag_match = 0                         # 结束模板选取阶段
            self.update()
            self.flag_play = 1
            self.pushButton_start.setIcon(self.icon_play)
            self.flag_first = 0
            self.flag_detect = 0                                    # 进入文件检测模式
            self.detecthread.flag_detect = 0
            self.flag_ROI = 0
            # 如果当前有线程正在运行，将所有线程停下来
            if self.videothread.isRunning():
                self.videothread.flag = 0
                self.videothread.quit()
                self.videothread.wait()
            if self.detecthread.isRunning():
                self.detecthread.flag = 0
                self.detecthread.quit()
                self.detecthread.wait()

                self.http_client.flag = 0
                self.http_client.quit()
                self.http_client.wait()

            if self.staticdetecthread.isRunning():
                self.staticdetecthread.flag = 0
                self.staticdetecthread.quit()
                self.staticdetecthread.wait()
            self.usb_monitor.params_init()
            self.usb_monitor.get_filename()
            try:      # 如果U盘有文件
                usb_img = self.usb_monitor.read_one_img()
                self.play_video({"img": usb_img})
                self.label_9.setText(str(self.usb_monitor.usb_img + 1) + '/' + str(self.usb_monitor.img_num))
            except:
                QMessageBox.warning(self, "Warning", "No Files in USB Device!")
                self.clear_ROI()


    def next_usb_img(self, direction):
        '''文件检测模式下的方向键槽函数'''
        if not self.flag_detect:                # 如果处于文件检测模式
            self.pushButton_start.setIcon(self.icon_play)
            self.flag_play = 1
            self.label_paint.init_Pixmap(self.label_12.size())      # 清空画布
            self.label_paint.init_draw_targets()                    # 清空图层。
            self.label_paint.ROI_rect = (0, 0, 0, 0)                # 初始化鼠标位置
            self.label_paint.flag_ROI = 1                           # 不允许画布显示多个图像
            self.label_paint.flag_match = 0                         #
            self.update()                                           # 刷新
            self.flag_first = 0                                     #
            self.flag_ROI = 0                                       # 切换图片以后需要重新设置ROI
            if self.detecthread.isRunning():
                self.detecthread.flag = 0
                self.detecthread.quit()
                self.detecthread.wait()

                self.http_client.flag = 0
                self.http_client.quit()
                self.http_client.wait()

            if self.staticdetecthread.isRunning():
                self.staticdetecthread.flag = 0
                self.staticdetecthread.quit()
                self.staticdetecthread.wait()
            if direction == 0:
                self.usb_monitor.usb_img -= 1           # 当前文件测次序需要改变
                try:      # 如果U盘有文件
                    cv2.waitKey(100)                    # 这里需要延时以下，否则图像显示可能有问题
                    usb_img = self.usb_monitor.read_one_img()       # 读取一张图片
                    self.play_video({"img": usb_img})
                except:
                    QMessageBox.warning(self, "Warning", "No Files in USB Device!")
            elif direction == 1:
                self.usb_monitor.usb_img += 1
                try:      # 如果U盘有文件
                    cv2.waitKey(100)
                    usb_img = self.usb_monitor.read_one_img()
                    self.play_video({"img": usb_img})
                except:
                    QMessageBox.warning(self, "Warning", "No Files in USB Device!")
            # 在label上显示当前文件的次序
            self.label_9.setText(str(self.usb_monitor.usb_img+1)+'/'+str(self.usb_monitor.img_num))


    def power(self):
        reply = QMessageBox.information(self,  # 使用infomation信息框
                                        "Power",
                                        "Whether Shutdown the Machine?",
                                        QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # os.system("shutdown")
            os.system("reboot")


    def get_temp(self):
        '''Linux下获取机器的CPU温度'''
        if self.system == "Linux":
            temp = psutil.sensors_temperatures()
            temp = temp['soc-thermal'][0][1]
            self.label_17.setText(str(temp))



    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.modifiers() == Qt.ControlModifier | Qt.ShiftModifier | Qt.AltModifier and \
                QKeyEvent.key() == Qt.Key_Q:
            self.setWindowFlags(QtCore.Qt.SubWindow)
            self.showNormal()
            # self.resizeEvent(QKeyEvent)


    def plot_patch(self):
        if not self.flag_play:
            scale_coe = self.origin_width / self.scaled_width
            a, b, c, d = self.label_paint.ROI_rect
            a, b = self.FromLabelToImage(a, b)
            c, d = int(c*scale_coe), int(d*scale_coe)
            self.detecthread.patch_Rect = (a, b, c, d)
            self.staticdetecthread.patch_Rect = (a, b, c, d)


    def update_software(self):
        if self.flag_usb:
            self.usb_monitor.update_software()
            QMessageBox.information(self, "Notice", "New Version Works after Reboot.")



    def draw_qchart1(self, ping_value):
        self.chart1.handleUpdate()
        self.chart1.update()
        self.chart1.ydata = ping_value



    def draw_qchart2(self, dic):
        self.chart2.handleUpdate()
        self.chart2.update()
        if dic["time"] == 1000:
            self.chart2.series.setColor(QColor(255, 0, 0))
        else:
            self.chart2.series.setColor(QColor(0, 0, 255))
        self.chart2.ydata = dic["time"]



    def draw_qchart3(self, conf):
        self.chart3.handleUpdate()
        self.chart3.update()
        self.chart3.ydata = conf



    def connect_http(self):     # pushbutton_http的槽函数
        if self.detecthread.isRunning() or self.staticdetecthread.isRunning():
            QMessageBox.information(self, "Notice", "Please quit detection mode when setting IP.")
        else:
            self.ip = self.lineEdit.text()
            self.ping_thread.ip = self.ip
            self.ping_thread.start()
            self.http_client.ip = self.ip
            print("connect: ", self.ip)
