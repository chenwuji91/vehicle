#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/26 13:03
# @Author  : chenwuji
# @File    : connection.py  描述:把pickle转换成文本的文件 主要考虑的是方便其他版本语言的处理
# @Software: PyCharm Community Edition


import cPickle as p
import glob
import os
import sys
from datetime import datetime
process_day = sys.argv[1]
# process_day = '2016_03_28'  #日期

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

import os
# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

'''
读取对应的网络拓扑数据
'''
def read_network():
    filepath = '../connection/' + process_day.replace('_','-') + '/' + '*.set.data'
    flist = glob.glob(filepath)
    for eachsecond in flist:
        basename = os.path.basename(eachsecond).strip('.set.data')
        current_time = secondsOfToday(basename)
        dataFile = file(eachsecond,'r')
        obj = p.load(dataFile)
        obj2 = map(lambda x:x[0] + '-' +x[1],obj)
        current_data = ','.join(obj2)
        makeDir('../connection_file/')
        writeToFile('../connection_file/' + basename, current_data)
        pass

def secondsOfToday(d1):
    d2 = d1.split(' ')[0] + ' ' + '00:00:00'
    dd1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    dd2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return (dd1-dd2).seconds

'''工具 把时间转换成标准时间'''
def time_retranslate(time_of_network):
    hour = time_of_network / 3600
    min = time_of_network % 3600 / 60
    seconds = time_of_network % 3600 % 60
    if hour < 10:
        hour = '0' + str(hour)
    if min < 10:
        min = '0' + str(min)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(hour) + ':' + str(min) + ':' + str(seconds)

if __name__ == '__main__':
    read_network()
    pass