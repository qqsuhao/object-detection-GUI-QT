# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, QtChart


class Ui_counting_Form(object):
    def setupUi(self, counting_Form):
        counting_Form.setObjectName("counting_Form")
        counting_Form.setWindowModality(QtCore.Qt.NonModal)
        counting_Form.resize(1100, 764)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(counting_Form.sizePolicy().hasHeightForWidth())
        counting_Form.setSizePolicy(sizePolicy)
        counting_Form.setMaximumSize(QtCore.QSize(1920, 1280))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        counting_Form.setFont(font)
        counting_Form.setAutoFillBackground(False)
        counting_Form.setStyleSheet("background:rgb(255, 255, 255)")
        counting_Form.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout = QtWidgets.QGridLayout(counting_Form)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tabWidget = QtWidgets.QTabWidget(counting_Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_12 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setFocusPolicy(QtCore.Qt.NoFocus)
        self.label_12.setAutoFillBackground(False)
        self.label_12.setLineWidth(10)
        self.label_12.setText("")
        self.label_12.setScaledContents(False)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.horizontalLayout_5.addWidget(self.tabWidget)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_5)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pushButton_power = QtWidgets.QPushButton(counting_Form)
        self.pushButton_power.setMinimumSize(QtCore.QSize(60, 60))
        self.pushButton_power.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pics/pics/power_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_power.setIcon(icon)
        self.pushButton_power.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_power.setFlat(True)
        self.pushButton_power.setObjectName("pushButton_power")
        self.horizontalLayout.addWidget(self.pushButton_power)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.label_16 = QtWidgets.QLabel(counting_Form)
        self.label_16.setMinimumSize(QtCore.QSize(60, 60))
        self.label_16.setMaximumSize(QtCore.QSize(60, 60))
        self.label_16.setLineWidth(1)
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap(":/pics/pics/temperature.png"))
        self.label_16.setScaledContents(True)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(counting_Form)
        self.label_17.setMinimumSize(QtCore.QSize(40, 60))
        self.label_17.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout.addWidget(self.label_17)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.pushButton_update = QtWidgets.QPushButton(counting_Form)
        self.pushButton_update.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pics/pics/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_update.setIcon(icon1)
        self.pushButton_update.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_update.setCheckable(False)
        self.pushButton_update.setChecked(False)
        self.pushButton_update.setDefault(False)
        self.pushButton_update.setFlat(True)
        self.pushButton_update.setObjectName("pushButton_update")
        self.horizontalLayout.addWidget(self.pushButton_update)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.line_3 = QtWidgets.QFrame(counting_Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_2.addWidget(self.line_3)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem7)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.label_15 = QtWidgets.QLabel(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_3.addWidget(self.label_15)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.pushButton_color = QtWidgets.QPushButton(counting_Form)
        self.pushButton_color.setAutoFillBackground(False)
        self.pushButton_color.setText("")
        self.pushButton_color.setFlat(True)
        self.pushButton_color.setObjectName("pushButton_color")
        self.horizontalLayout_3.addWidget(self.pushButton_color)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.label_13 = QtWidgets.QLabel(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_6.addWidget(self.label_13)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.spinBox = QtWidgets.QSpinBox(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox.setFont(font)
        self.spinBox.setProperty("value", 4)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_6.addWidget(self.spinBox)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem14)
        self.pushButton_http = QtWidgets.QPushButton(counting_Form)
        self.pushButton_http.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pics/pics/connect.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_http.setIcon(icon2)
        self.pushButton_http.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_http.setAutoDefault(False)
        self.pushButton_http.setFlat(True)
        self.pushButton_http.setObjectName("pushButton_http")
        self.horizontalLayout_7.addWidget(self.pushButton_http)
        self.lineEdit = QtWidgets.QLineEdit(counting_Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_7.addWidget(self.lineEdit)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem15)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem16 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem16)
        spacerItem17 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem17)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem18)
        self.pushButton_usb = QtWidgets.QPushButton(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_usb.setFont(font)
        self.pushButton_usb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pics/pics/usb_off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_usb.setIcon(icon3)
        self.pushButton_usb.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_usb.setFlat(True)
        self.pushButton_usb.setObjectName("pushButton_usb")
        self.horizontalLayout_4.addWidget(self.pushButton_usb)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem19)
        self.pushButton_usb_left = QtWidgets.QPushButton(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_usb_left.setFont(font)
        self.pushButton_usb_left.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pics/pics/left_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_usb_left.setIcon(icon4)
        self.pushButton_usb_left.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_usb_left.setFlat(True)
        self.pushButton_usb_left.setObjectName("pushButton_usb_left")
        self.horizontalLayout_4.addWidget(self.pushButton_usb_left)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem20)
        self.pushButton_usb_right = QtWidgets.QPushButton(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_usb_right.setFont(font)
        self.pushButton_usb_right.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/pics/pics/arrow_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_usb_right.setIcon(icon5)
        self.pushButton_usb_right.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_usb_right.setFlat(True)
        self.pushButton_usb_right.setObjectName("pushButton_usb_right")
        self.horizontalLayout_4.addWidget(self.pushButton_usb_right)
        spacerItem21 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem21)
        self.label_9 = QtWidgets.QLabel(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_4.addWidget(self.label_9)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem22)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem23 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem23)
        spacerItem24 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem24)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem25)
        self.pushButton_stop = QtWidgets.QPushButton(counting_Form)
        self.pushButton_stop.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/pics/pics/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_stop.setIcon(icon6)
        self.pushButton_stop.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_stop.setFlat(True)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout_2.addWidget(self.pushButton_stop)
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem26)
        self.pushButton_start = QtWidgets.QPushButton(counting_Form)
        self.pushButton_start.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/pics/pics/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon7.addPixmap(QtGui.QPixmap(":/pics/pics/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_start.setIcon(icon7)
        self.pushButton_start.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_start.setAutoRepeat(False)
        self.pushButton_start.setAutoExclusive(False)
        self.pushButton_start.setAutoDefault(False)
        self.pushButton_start.setDefault(False)
        self.pushButton_start.setFlat(True)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout_2.addWidget(self.pushButton_start)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem27)
        self.pushButton_save = QtWidgets.QPushButton(counting_Form)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/pics/pics/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_save.setIcon(icon8)
        self.pushButton_save.setIconSize(QtCore.QSize(50, 50))
        self.pushButton_save.setAutoDefault(False)
        self.pushButton_save.setFlat(True)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout_2.addWidget(self.pushButton_save)
        spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem28)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.line = QtWidgets.QFrame(counting_Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        spacerItem29 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem29)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.graphicsView = QtChart.QChartView(counting_Form)
        self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.setTabletTracking(True)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout_3.addWidget(self.graphicsView)
        self.graphicsView_2 = QtChart.QChartView(counting_Form)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout_3.addWidget(self.graphicsView_2)
        self.graphicsView_3 = QtChart.QChartView(counting_Form)
        self.graphicsView_3.setObjectName("graphicsView_3")
        self.verticalLayout_3.addWidget(self.graphicsView_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.setStretch(3, 5)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.horizontalLayout_8.setStretch(0, 7)
        self.horizontalLayout_8.setStretch(2, 2)
        self.gridLayout.addLayout(self.horizontalLayout_8, 1, 1, 2, 1)
        spacerItem30 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem30, 2, 2, 1, 1)
        spacerItem31 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem31, 3, 1, 1, 1)

        self.retranslateUi(counting_Form)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton_stop.clicked.connect(counting_Form.clear_ROI)
        self.pushButton_start.clicked.connect(counting_Form.play_and_pause)
        self.spinBox.valueChanged['int'].connect(counting_Form.penwidth_choose)
        QtCore.QMetaObject.connectSlotsByName(counting_Form)

    def retranslateUi(self, counting_Form):
        _translate = QtCore.QCoreApplication.translate
        counting_Form.setWindowTitle(_translate("counting_Form", "Gaga"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("counting_Form", "Tab "))
        self.label_17.setText(_translate("counting_Form", "0"))
        self.label_15.setText(_translate("counting_Form", "PaintColor"))
        self.label_13.setText(_translate("counting_Form", "Linewidth"))
        self.label_9.setText(_translate("counting_Form", "0/0"))
import ui.pic_rc
