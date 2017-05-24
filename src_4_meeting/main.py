#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/16 15:03
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition
# @Notice: 计算的时候基于一个假设,就是在单个网格内的是都可以通讯的  即position5内的网格全部是可以通讯的
import csv
# import thread
from time import ctime,sleep
import pandas as pd
# import numpy as np
import math
from square import *
# communicate_dis = 10     #通讯距离为10个网格  50/5  50米  5米一个小网格 就是10个网格的通讯距离
cpu_core_num = 8  #执行多线程函数的时候 cpu核心的数量
communication_square = 12 # 10*5就是50米   50/5   #允许的通讯距离 单位是网格数 因为网格固定的是5米一个网格  就是比如通讯距离是50 那么通讯网格就是10个网格
'''基于程序设定的通讯距离,找到一个中心网格周围所有的偏移网格'''
def __init_relative_square():
    in_range = set()
    for i in range(communication_square + 1):
        for j in range(communication_square + 1):
            if math.sqrt(i**2+j**2) < communication_square:
                in_range.add((i,j))
                in_range.add((-i, j))
                in_range.add((i, -j))
                in_range.add((-i, -j))
    in_range.remove((0,0))  #这样就不包含本网格
    return in_range

around_square_base = __init_relative_square()

def get_relative(center_square):
    change_index = map(lambda x:(center_square[0] + x[0], center_square[1] + x[1]), around_square_base)
    return filter(lambda x:x[0] >= 0 and x[0] < eve_num_of_line and x[1] >=0 and x[1] < eve_num_of_col, change_index)


def process_single_core(filename = '../data/2016-03-28'):
    csvfile = csv.reader(file(filename), delimiter=';')
    for eachline in csvfile:
        __process_data(eachline)


'''
处理每一秒的数据,每一秒的数据单独进行处理
'''
def __process_data(eachline):
    print eachline[0]
    current_time = eachline[0]
    data_list = map(lambda x:x.split(','), eachline[1:])
    detailed_position = {}  #每个车在这一秒的位置信息 详细记录了每个车什么时刻在哪个网格
    map(lambda x:detailed_position.setdefault(x[0],x[1]),data_list)
    def remove_details(x):  #定义函数转换坐标信息
        x[1] = (int(x[1].split('-')[0]),int(x[1].split('-')[1]))
    map(remove_details, data_list)  #位置信息用元组表示
    alist = pd.DataFrame(data_list, columns= ['vid','position'])
    position_dict = alist.set_index('vid').groupby(['position']).groups

    all_edge = set()  #保存所有的可以互相通讯的车的集合
    for eachsquare in position_dict:
        current_square_vehicle = position_dict[eachsquare]
        around_square = get_relative(eachsquare)
        around_vehicle = reduce(lambda x,y:x+y,map(lambda x:position_dict[x] if position_dict.__contains__(x) else [],around_square))
        for vehicle_center in current_square_vehicle:
            for vehicle_around in around_vehicle:
                all_edge.add((vehicle_center,vehicle_around))
                all_edge.add((vehicle_around, vehicle_center))

    makeDir('../connection/' + current_time.split(' ')[0] + '/')
    makeDir('../detailed_position/' + current_time.split(' ')[0] + '/')
    toFileWithPickle('../detailed_position/' + current_time.split(' ')[0] + '/' + current_time + '.dict', detailed_position)
    toFileWithPickle('../connection/' + current_time.split(' ')[0] + '/' + current_time + '.set', all_edge)



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


if __name__ == '__main__':
    # all_data = read_file()
    import sys
    if len(sys.argv) > 1:
        process_single_core(sys.argv[1])
    else:
        process_single_core()