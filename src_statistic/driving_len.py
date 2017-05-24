#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/27 14:51
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition
# @说明: 统计车辆在每天行驶的长度 作出统计图表

import csv
import glob
import matplotlib.pyplot as plt
import os

def read_file(filename = '../movingSeq/2016-03-03.txt'):
    vehicle_len = []
    dict_len = {}
    csvfile = csv.reader(file(filename), delimiter=';')
    for eachline in csvfile:
        # vehicle_len.append((eachline[0],len(eachline[1:])))
        if len(eachline[1:]) > 10000:
            continue
        if not dict_len.__contains__(len(eachline[1:])):
            dict_len[len(eachline[1:])] = 1
        else:
            dict_len[len(eachline[1:])] += 1
    return vehicle_len,dict_len


def plot(dict_plot, filename):
    X = dict_plot.keys()
    Y = dict_plot.values()
    # X = [0, 1, 3, 2, 4, 5]
    # Y = [222, 42, 1, 664, 454, 334]
    plt.bar(X, Y, 0.4, color="green")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("bar chart")
    # plt.show()
    plt.savefig(filename + '-10000.png')
    plt.close()


if __name__ == '__main__':
    flist = glob.glob('../movingSeq/*')
    for eachfile in flist:
        vehicle_len, dict_len = read_file(eachfile)
        plot(dict_len, os.path.basename(eachfile))
        pass