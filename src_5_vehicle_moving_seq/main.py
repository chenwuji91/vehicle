#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/24 14:12
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition

import csv
from datetime import datetime
import os
import glob

def process_file(filename = '../data/2016-03-28'):
    folder_name = os.path.basename(filename)
    makeDir('../movingSeq/' + '/' + folder_name + '/')
    csvfile = csv.reader(file(filename), delimiter=';')
    for eachline in csvfile:
        current_time = eachline[0]
        time_current = secondsOfToday(current_time)
        data_list = map(lambda x: x.split(','), eachline[1:])
        for eachpair in data_list:
            writeToFile('../movingSeq/' + folder_name + '/' + eachpair[0], str(time_current) + ',' + eachpair[1])
    return '../movingSeq/' + folder_name + '/'

def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def secondsOfToday(d1):
    d2 = d1.split(' ')[0] + ' ' + '00:00:00'
    dd1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    dd2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return (dd1-dd2).seconds

def generate_one_file(foldername):
    flist = glob.glob(foldername+'*')
    for filename in flist:
        output_str = os.path.basename(filename)
        csvfile = csv.reader(file(filename), delimiter=',')
        for t,p in csvfile:
            output_str = output_str + ';' + t + ',' + p
        writeToFile('../movingSeq/' + foldername.split('/')[2] + '.txt',output_str)
    os.system('rm -r ' + foldername)



if __name__ == '__main__':
    # flist = glob.glob('../data/*')
    # for eachfile in flist:
    #     generate_one_file(process_file(eachfile))
    generate_one_file(process_file())