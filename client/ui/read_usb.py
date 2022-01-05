# -*- coding:utf8 -*-
# @TIME     : 2020/8/9 17:59
# @Author   : Hao Su
# @File     : read_usb.py

'''
检查usb是否插入
读取usb中的图片文件
'''
import cv2
import numpy as np
import psutil
import os
import platform


class ImageTargets():
    '''图片以及对应的识别目标'''
    def __init__(self, img, targets_circ):
        self.img = img
        self.targets_circ = targets_circ


class USB():
    def __init__(self):
        self.usb_path = None            # usb设备的路径,这个不能放在params_init中
        self.params_init()


    def params_init(self):
        self.flag_usb = 0               # 表示有usb设备插入
        self.usb_list = []              # 所有USB接口的工作情况
        self.filename = []              # 存放所有文件名，列表
        self.image_targets_list = []    # 存放所有图片对应的对象
        self.img_num = 0                # 图片数量
        self.usb_img = 0         # 从usb读取出来的图像的次序
        self.img = np.array([[]])       # 图片缓存



    def check_usb(self):
        self.usb_list = psutil.disk_partitions()
        try:
            if platform.system() == "Windows":
                index = ["removable" in item.opts for item in psutil.disk_partitions()].index(True)
                self.flag_usb = 1
                self.usb_path = self.usb_list[index].mountpoint
            elif platform.system() == "Linux":
                index = ["/dev/sda1" == item.device for item in psutil.disk_partitions()].index(True)
                self.flag_usb = 1
                self.usb_path = self.usb_list[index].mountpoint
        except ValueError:
            index = -1
            self.flag_usb = 0
            self.usb_path = None
        return self.flag_usb


    def get_filename(self):
        '''        # 获取指定目录下的所有指定后缀的文件名
         :param suffix： [bmp, jpg, png, tif, jpeg]
         '''
        if self.usb_path:
            suffix = ['.bmp', '.jpg', '.png', '.jpeg']
            f_list = os.listdir(self.usb_path)  # 返回文件名
            for i in f_list:
                # os.path.splitext():分离文件名与扩展名
                if os.path.splitext(i)[1] in suffix:
                    self.filename.append(i)
            self.img_num = len(self.filename)


    def read_all_img(self):
        if self.filename:
            for item in self.filename:
                img = cv2.imread(self.usb_path+'/'+item)
                imagetargets = ImageTargets(img, np.array([[]]))
                self.image_targets_list.append(imagetargets)


    def read_one_img(self):
        self.usb_img = self.usb_img % self.img_num
        self.img = cv2.imread(self.usb_path + '/' + self.filename[self.usb_img])
        return self.img


    def update_software(self):
        '''
        更新软件
        :return:
        '''
        filename =[]
        if self.usb_path:
            suffix = ['.py', '.pyc', '.so', '.c']
            f_list = os.listdir(self.usb_path)  # 返回文件名
            for i in f_list:
                if os.path.splitext(i)[1] in suffix:
                    filename.append(i)
                if platform.system() == "Linux":
                    os.system("cp "+self.usb_path+"/* /home/pi/counting_GUI")
                    # for i in range(len(filename)):
                    #     os.system("cp "+self.usb_path+"/"+filename[i]+ " /home/pi/counting_GUI")




