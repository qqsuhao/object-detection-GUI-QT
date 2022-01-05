# -*- coding:utf8 -*-
# @TIME     : 2021/12/18 14:45
# @Author   : Hao Su
# @File     : chart.py

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
import time

class Chart(QChart):
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)
        self.xRange = 100
        self.sampleRate = 2
        self.counter = 0
        self.seriesList = []
        self.temp_y = []
        self.ydata = 0
        # self.legend().show()
        self.legend().setVisible(False)

        self.axisX = QValueAxis()
        self.axisX.setRange(0, self.xRange)
        self.axisX.setLabelFormat("%d")
        # self.axisX.setVisible(False)
        self.addAxis(self.axisX, Qt.AlignBottom)
        # self.setAxisX(self.axisX, series)

        self.axisY = QValueAxis()
        self.axisY.setRange(-1, 1)
        self.axisY.setLabelFormat("%.1f")
        self.axisY.setTickCount(3)
        self.addAxis(self.axisY, Qt.AlignLeft)
        # self.setAxisY(self.axisY, series)

        self.series = QLineSeries()
        self.series.setColor(QColor(0, 0, 255))
        # self.series.setName("生成300~1000随机数")
        # self.series.setUseOpenGL(True)
        self.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)



    def handleUpdate(self):
        ydata = self.ydata
        if (self.counter < self.xRange):
            for i in range(self.sampleRate):
                self.temp_y.append(ydata)
                self.axisY.setRange(min(self.temp_y), max(self.temp_y))
                self.series.append(self.counter + i, ydata)
        else:
            points = self.series.pointsVector()
            y_temp = [0] * (len(points) - self.sampleRate)
            for i in range(len(points) - self.sampleRate):
                points[i].setY(points[i + self.sampleRate].y())
                y_temp[i] = points[i + self.sampleRate].y()
            for i in range(self.sampleRate):
                points[len(points) - (self.sampleRate - i)].setY(ydata)
            self.series.replace(points)
            self.axisY.setRange(min(y_temp), max(y_temp))
        # self.series.setUseOpenGL(True)
        self.counter += self.sampleRate



class WorkThread(QThread):
    _signal_updateUI = pyqtSignal()

    def __init__(self, parent=None, t=1):
        super(WorkThread, self).__init__(parent)
        self.qmut = QMutex()
        self.isexit = False
        self.t = t

    def run(self):
        while (True):
            self.qmut.lock()
            if (self.isexit):
                break
            self.qmut.unlock()

            self._signal_updateUI.emit()
            time.sleep(self.t)
        self.qmut.unlock()

    def stop(self):
        # 改变线程状态与终止
        self.qmut.lock()
        self.isexit = True
        self.qmut.unlock()
        self.wait()