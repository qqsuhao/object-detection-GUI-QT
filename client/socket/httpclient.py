#coding:utf-8
import cv2
import json
import requests
import numpy as np
import time
import threading
import subprocess
import re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def get_ping_result(ip_address):
    p = subprocess.Popen(["ping.exe", ip_address], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    out = p.stdout.read().decode('gbk')

    reg_receive = '已接收 = \d'
    match_receive = re.search(reg_receive, out)

    receive_count = -1

    if match_receive:
        receive_count = int(match_receive.group()[6:])

    if receive_count > 0:  # 接受到的反馈大于0，表示网络通
        reg_min_time = '最短 = \d+ms'
        reg_max_time = '最长 = \d+ms'
        reg_avg_time = '平均 = \d+ms'

        match_min_time = re.search(reg_min_time, out)
        min_time = int(match_min_time.group()[5:-2])

        match_max_time = re.search(reg_max_time, out)
        max_time = int(match_max_time.group()[5:-2])

        match_avg_time = re.search(reg_avg_time, out)
        avg_time = int(match_avg_time.group()[5:-2])
        return [receive_count, min_time, max_time, avg_time]
    else:
        print('网络不通，目标服务器不可达！')
        return [0, 9999, 9999, 9999]


class PingThread(QThread):
    ping_signal = pyqtSignal(int)

    def __init__(self, ip):
        super(PingThread, self).__init__()
        self.ping = 0
        self.flag = 1
        self.ip = ip

    def run(self):
        while self.flag:
            _, _, _, self.ping = get_ping_result(self.ip)
            # print(self.ping)
            self.ping_signal.emit(self.ping)


class HttpClient(QThread):
    http_signal = pyqtSignal(dict)


    def __init__(self, ip, port="8081"):
        super(HttpClient, self).__init__()
        self.ip = ip
        self.port = port
        self.headers = {'Connection': 'keep-alive'}
        self.img = None
        self.qmut = QMutex()
        self.flag = 1


    def encodeimg(self, img):
        encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
        result, imgencode = cv2.imencode('.png', img, encode_param)
        data = np.array(imgencode)
        data_Bytes = data.tobytes()
        return data_Bytes


    def parse_message(self):
        pass


    def post(self):
        self.qmut.lock()
        if self.img is None:
            self.qmut.unlock()
            return
        res = {"image": str(self.encodeimg(self.img))}  # img是ndarray，无法直接用base64编码，否则会报错
        self.qmut.unlock()
        start_time = time.time()
        message = requests.post("http://"+self.ip+":"+self.port, headers=self.headers, data=json.dumps(res))
        duration = time.time() - start_time
        print('duration:[%.0fms]' % (duration * 1000))
        self.http_signal.emit({"time": duration*1000})
        data_Bytes = json.loads(message.data)
        loc = np.frombuffer(data_Bytes, dtype="float16")
        print(loc)
        return loc

    def run(self):
        while self.flag:
            self.post()

if __name__ == "main":
    httpclient = HttpClient(ip="127.0.0.1")
    httpclient.post()



