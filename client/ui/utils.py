# -*- coding:utf8 -*-
# @TIME     : 2021/12/18 16:44
# @Author   : Hao Su
# @File     : utils.py

import psutil
import time


def get_key():
    key_info = psutil.net_io_counters(pernic=True).keys()
    recv = {}
    sent = {}
    for key in key_info:
        recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)
        sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)
    return key_info, recv, sent


def get_rate(func):
    key_info, old_recv, old_sent = func()
    time.sleep(0.001)
    key_info, now_recv, now_sent = func()
    net_in = {}
    net_out = {}
    for key in key_info:
        # float('%.2f' % a)
        net_in.setdefault(key, float('%.2f' % ((now_recv.get(key) - old_recv.get(key)) / 1024)))
        net_out.setdefault(key, float('%.2f' % ((now_sent.get(key) - old_sent.get(key)) / 1024)))

    return key_info, net_in, net_out


def get_speed():
    key_info, net_in, net_out = get_rate(get_key)
    in_speed = 0
    out_speed = 0
    for key in key_info:
        # lo 是linux的本机回环网卡，以太网是我win10系统的网卡名
        if key != 'lo' or key == '以太网':
            # print('%s\nInput:\t %-5sKB/s\nOutput:\t %-5sKB/s\n' % (key, net_in.get(key), net_out.get(key)))
            in_speed += net_in.get(key)
            out_speed += net_out.get(key)
    return in_speed, out_speed


def speed_test():
    s1 = psutil.net_io_counters(pernic=True)['WLAN 2']
    time.sleep(0.001)
    s2 = psutil.net_io_counters(pernic=True)['WLAN 2']
    result = s2.bytes_recv - s1.bytes_recv
    #除法结果保留两位小数
    return result / 1024
