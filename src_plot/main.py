#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/21 13:14
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition


import cPickle as p
import os
import glob
import matplotlib.pyplot as pl
import square

def getObj(path):
    dataFile = file(path,'r')
    obj = p.load(dataFile)
    return obj

def generate_network(filebasename = '2016-03-26 07_18_29'):
    pair_set = getObj('../connection/2016-03-28/'+filebasename +'.set.data')
    position_dict = getObj('../detailed_position/2016-03-28/'+ filebasename +'.dict.data')
    position_list = map(lambda x:[position_dict[x[0]],position_dict[x[1]]],list(pair_set))
    position_details = map(lambda x:[square.getWG_centerLonLat(x[0]), square.getWG_centerLonLat(x[1])],position_list)
    plot(position_details, filebasename)

def plot(details_position, filebasename):
    print 'ploting...',filebasename
    color_list = ['k-o','g-*','y-*','m-.','k-.','b-.','g-.','y-..','m-.','k-.']
    fig = pl.figure(figsize=(90, 45))
    pl.clf()
    for eachpair in details_position:
        pl.plot([eachpair[0][0]*100,eachpair[1][0]*100],[eachpair[0][1]*100,eachpair[1][1]*100],color_list[0],linewidth=3) #,color_list[1]
    pl.grid(True)
    # pl.xlim(X.min() * 1.1, X.max() * 1.1)
    # pl.ylim(C.min() * 1.1, C.max() * 1.1)
    makeDir('../plot')
    pl.savefig('../plot' + filebasename)
    pl.close()

import os
# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

if __name__ == '__main__':
    flist = glob.glob('../connection/2016-03-28/*')
    for eachfile in flist:
        generate_network(os.path.basename(eachfile).split('.')[0])
    pass