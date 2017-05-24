#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/26 21:37
# @Author  : chenwuji
# @File    : vehicle_id_everyday.py  统计每天车的id以及被卡口拍摄下来的长度 再看交集有多少  这个从原始数据里面做相关的处理
# @Software: PyCharm Community Edition

import glob
import pickle as p
import os
import csv
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)


def process():
    flist = glob.glob('../data/*')
    for eachfile in flist:
        print 'current process:',eachfile
        basename = os.path.basename(eachfile)
        vehicle_lukou_dict = {}
        csvfile = csv.reader(file(eachfile), delimiter=',')
        for d1,d2,d3,d4,d5,d6,d7 in csvfile:
            if not vehicle_lukou_dict.__contains__(d1):
                vehicle_lukou_dict[d1] = 1
            else:
                vehicle_lukou_dict[d1] += 1
        makeDir('vehicle_appear_time/')
        toFileWithPickle('vehicle_appear_time/' + basename,vehicle_lukou_dict)



if __name__ == '__main__':

    pass