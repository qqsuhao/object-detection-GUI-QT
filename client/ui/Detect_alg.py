# -*- coding:utf8 -*-
# @TIME     : 2020/8/2 23:40
# @Author   : Hao Su
# @File     : Detect_alg.py

'''
ROI自动监测算法
菌落计数检测算法
'''

import cv2
import numpy as np
import copy


def FindROI(img):
    '''
    :param img:
    :return: 圆心坐标和圆半径，如果找不到就都返回0
    '''
    circle_1 = None
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayImage = cv2.resize(grayImage, (grayImage.shape[1] >> 1, grayImage.shape[0] >> 1))
    circle_1 = cv2.HoughCircles(grayImage, cv2.HOUGH_GRADIENT, 1, 100,
                                param1=100, param2=30, minRadius=20, maxRadius=240)
    if circle_1 is not None:
        circle_2 = np.uint16(np.around(circle_1[0, :, :]))
        return circle_2[0, 0]<<1, circle_2[0, 1]<<1, circle_2[0, 2]<<1
    else:
        return 0, 0, 0


def dist_to_center(contour, center):
    '''
    :param contour: 轮廓
    :param center: ROi的圆心
    :return: 距离
    '''
    mu = cv2.moments(contour)
    x = int(mu['m10'] / (mu['m00'] + 0.0000001))  # 表示列数，是横坐标
    y = int(mu['m01'] / (mu['m00'] + 0.0000001))
    center = np.array(center).astype('uint64')
    dist = np.sqrt((y - center[0]) ** 2 + (x - center[1]) ** 2)
    return dist


def distance_to_center(image, contour):
    drawing = 255 + np.zeros_like(image)
    cv2.drawContours(drawing, contour, -1, (0, 0, 0), 1)
    drawing = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
    # 确定轮廓的重心
    mu = cv2.moments(contour)
    cx = int(mu['m10'] / (mu['m00']))  # 表示列数，是横坐标
    cy = int(mu['m01'] / (mu['m00']))

    # 计算轮廓到重心的距离
    '''
    这里遇到一个问题：轮廓不总是一个像素点，也就是说轮廓是有厚度的
    '''
    label = np.where(drawing == 0)
    # 注意此处矩阵元素的下标与在二维平面的坐标是反的，行表示纵坐标
    location = np.array(label).T
    location = location[:, ::-1]
    location = location.astype("float64")
    center = np.array([[cx, cy]])
    center = np.tile(center, (location.shape[0], 1))
    center = center.astype("float64")
    dist = (location - center) ** 2
    dist = np.sqrt(dist.sum(axis=1))
    return dist


# template matching and processing
def match_templates(img_test, img_patch, th2=60):
    corr_result = cv2.matchTemplate(img_test, img_patch, cv2.TM_CCOEFF_NORMED)
    cv2.normalize(corr_result, corr_result, 0, 1, cv2.NORM_MINMAX, -1)
    corr_image = np.array(corr_result * 255, dtype=np.uint8)
    matchednot_image = cv2.bitwise_not(corr_image)
    img_inv = cv2.threshold(matchednot_image, th2, 255, cv2.THRESH_BINARY)[1]
    return img_inv
    # return matchednot_image


# crop image for matching
def crop_AreaRect(gray, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    img_crop = gray[y:y + h, x:x + w]
    return img_crop


# skip circles similar radius
def delete_similarCircles(Circ_cntrs, Circ_r, th):
    init_pos = np.int8(np.floor(len(Circ_r) / 2))
    Circ_unique = [Circ_cntrs[init_pos]]
    r0 = [Circ_r[init_pos]]
    for i, r in enumerate(Circ_r):
        if np.min(r0) / (r + 1e-4) > th / 10:
            Circ_unique.append(Circ_cntrs[i])
            r0.append(r)
        elif r / (np.max(r0) + 1e-4) > th / 10:
            Circ_unique.append(Circ_cntrs[i])
            r0.append(r)
    return Circ_unique, r0


# detect overlapped circles
def detect_overlappedCircles(r_list, Circ_r):
    r_small = r_list < Circ_r
    loc_small = [i for i, x in enumerate(r_small) if x]
    r_sel = Circ_r[r_small]
    if len(r_sel > 1):  # reserve the larger one
        r_small[loc_small[np.argmax(r_sel)]] = False
    return r_small


# delete overlapped circles
def delete_overlappedCircles(R_Bool, Circ_Rsvd, Circ_r):
    r_bool = R_Bool[:, 0]
    for i in range(1, len(R_Bool)):
        r_bool = np.bitwise_or(r_bool, R_Bool[:, i])
    Circ_noOVLP = []
    Circ_rNoOVLP = []
    for i in range(len(r_bool)):
        if r_bool[i] == False:
            Circ_noOVLP.append(Circ_Rsvd[i])
            Circ_rNoOVLP.append(Circ_r[i])
    return Circ_noOVLP, Circ_rNoOVLP


def nothing(x):
    pass


def Detect_alg(img, patch, flag_play, th2, binthreshold, minArea=10, maxArea=10000):
    '''
    :param img:
    :param flag_play:   是否处于连续检测阶段
    :param th: 相似度门限
    :param th2: 模板匹配门限
    :param th4: ROI边缘处需要忽略的区域大小
    :param binthreshold: 二值化门限
    :param minArea:
    :param maxArea:
    :return:
    '''
    print("Detecting")
    minArea_patch = minArea
    maxArea_patch = maxArea
    Circ_noOVLP = []
    img_copy = img.copy()
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binImage = cv2.threshold(grayImage, binthreshold, 255, cv2.THRESH_BINARY)

    patch_img = crop_AreaRect(binImage, patch)
    # _, mask = cv2.threshold(patch_img, 0, 255, cv2.THRESH_OTSU)
    mask = patch_img
    # mask = 255 - mask
    # img_patch = cv2.bitwise_and(patch_img, patch_img, mask=mask)
    if cv2.__version__[0] == '3':
        _, contour, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contour, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(patch_img, contour[0], -1, (0, 0, 255), -1)
    if contour:
        rect = cv2.boundingRect(contour[0])
        img_patch = crop_AreaRect(mask, rect)

        # 模板匹配
        img_match = match_templates(255-binImage, 255-img_patch, th2)
        if cv2.__version__[0] == '3':
            _, contours, _ = cv2.findContours(img_match, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        else:
            contours, _ = cv2.findContours(img_match, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            r = cv2.minEnclosingCircle(cnt)[1]
            cnt += int(r)  # offset the template match which returns the match quality at the corner, not center (opencv is shitty)

        # 筛选匹配结果
        for j in range(len(contours))[::-1]:
            cnt = contours[j]
            area = cv2.contourArea(cnt)
            mRect = cv2.minAreaRect(cnt)[1]  # (center), (width,height), angle
            circ_ratio = np.abs(mRect[1] - mRect[0]) / (np.min(mRect) + 1e-4)
            if (area <= minArea or area >= maxArea or cv2.minEnclosingCircle(cnt)[1]>60 or circ_ratio>0.3):
                del contours[j]
                continue


        contoursArray = img.copy()  # np.zeros((rows, cols), np.uint8) # img
        cv2.drawContours(contoursArray, contours, -1, (0, 0, 255), 1)
        contoursNum = len(contours)
        cv2.putText(contoursArray, str(contoursNum), (25, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        print("No Template!")
        contoursArray = img.copy()
        contoursNum = 0
        contours = []

    if flag_play:
        return contoursArray, contoursNum
    else:
        if contours:
            targets_cir = np.zeros((len(contours), 3))
            for i, cnt in enumerate(contours):
                circ_cent = cv2.minEnclosingCircle(cnt)[0]
                circ_radius = int(cv2.minEnclosingCircle(cnt)[1])
                targets_cir[i, 0] = int(circ_cent[0])
                targets_cir[i, 1] = int(circ_cent[1])
                targets_cir[i, 2] = circ_radius
        else:
            targets_cir = np.array([[]])
        return img_copy, targets_cir



    # if flag_play:
    #     return img, 0
    # else:
    #     target = np.array([[120, 110, 20, 20, 0],
    #                        [70, 34, 20, 20, 0],
    #                        [269, 168, 20, 20, 0]])
    #     # target用于存放检测结果，前面两列是左上顶点坐标， 然后是横宽和列宽，最后是绘制线宽
    #     # 绘制线宽在绘制的时候进行确认；圆半径由轮廓的最小外界矩形的最短边长确定
    #     return img, target