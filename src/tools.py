#-*- coding: UTF-8 -*-
'''
@author: chenwuji
常用工具类
'''

#时间处理的相关工具
from datetime import datetime
def timeTranslate(date):

    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/6) + 1
    return timeSplit

from datetime import datetime
from datetime import timedelta
def increase_several_seconds(ds, increase_seconds):
    ds = ds.split('.')[0]
    incre = timedelta(seconds = increase_seconds)
    ds2 = datetime.strptime(ds, "%Y-%m-%d %H:%M:%S") + incre
    return str(ds2)

def decrease_several_seconds(ds, increase_seconds):
    incre = timedelta(seconds = increase_seconds)
    ds2 = datetime.strptime(ds, "%Y-%m-%d %H:%M:%S") - incre
    return str(ds2)

def time_hour_min(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    return h,m

def timeTranslate_half_hour(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/30) + 1
    return timeSplit

def timeRetranslate(time):
    time = int(time)
    hour = int(time/10)
    minute = int(time%10) * 6
    return str(hour) + ':' + str(minute)

def getDay(date):
    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day
    return d

def intervalofSeconds(d1, d2):
    d1 = d1.split('.')[0]
    d2 = d2.split('.')[0]
    dd1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    dd2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return (dd2-dd1).seconds



#计算类
from math import radians, cos, sin, asin, sqrt
def calculate(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000


#IO类
import cPickle as p
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

import os
# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def getObj(path):
    dataFile = file(path,'r')
    obj = p.load(dataFile)
    return obj

def translate_potential_path(potential_list):#将点的表示转换成为边的一个表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append((eachS[i],eachS[i + 1]))
        translated_set.append(each_translated_path)
    return translated_set

def re_translate_potential_path(potential_list):#将边的表示转换成为点的表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append(eachS[i][0])
        each_translated_path.append(eachS[len(eachS)-1][0])
        each_translated_path.append(eachS[len(eachS)-1][1])
        translated_set.append(each_translated_path)
    return translated_set

def re_translate_one_potential_path(potential_list):#将边的表示转换成为点的表示
    translated_set = []
    for eachS in potential_list:
        translated_set.append(eachS[0])
    translated_set.append(eachS[1])
    return translated_set






if __name__ == '__main__':
    mu1 = 0
    sig1 = 1
    mu2 = 0
    sig2 = 1
    import random
    import numpy as np
    import math
    count = 0
    for i in range(1000000):
        x = np.random.normal(mu1, sig1)
        y= np.random.normal(mu2, sig2)
        if (x * x + y * y - 1)*(x * x + y * y - 1) - x * x * y * y < 0:
            count += 1

    print float(count)/1000000.0

    # print increase_several_seconds('2015-03-07 16:10:10', 24)
    # ttt = '2015-02-03 12:21:21'
    # print ttt[10:19]
    # print timeRetranslate(84)
    # print intervalofSeconds('2015-03-07 6:10:10','2015-03-07 06:12:10')
    # # print timeRetranslate(73)
    # print re_translate_one_potential_path([('1007', '1009'), ('1009', '1122')])

# The following calculate direction:
# right1 = top1 = right2 = top2 = 0.0
#
# for i in range(len(record1) - 1):
#     right1 = right1 + lukou_info[record1[i + 1]][0] - lukou_info[record1[i]][0]
#     top1 = top1 + lukou_info[record1[i + 1]][1] - lukou_info[record1[i]][1]
# for i in range(len(record2) - 1):
#     right2 = right2 + lukou_info[record2[i + 1]][0] - lukou_info[record2[i]][0]
#     top2 = top2 + lukou_info[record2[i + 1]][1] - lukou_info[record2[i]][1]
#
# if abs(right1) > abs(top1):
#     judge1 = right1
# else:
#     judge1 = top1
#
# if abs(right2) > abs(top2):
#     judge2 = right2
# else:
#     judge2 = top2
# if judge1 * judge2 > 0: