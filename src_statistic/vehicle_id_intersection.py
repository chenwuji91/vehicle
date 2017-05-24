#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/4/26 23:47
# @Author  : chenwuji
# @File    : vehicle_id_intersection.py  继续统计,求交集
# @Software: PyCharm Community Edition

#IO类
import cPickle as p
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()


def getObj(path):
    dataFile = file(path,'r')
    obj = p.load(dataFile)
    return obj

def statistic(date1,date2):
    data1 = getObj('./vehicle_appear_time/2016-03-'+date1+'.csv.data')
    data2 = getObj('./vehicle_appear_time/2016-03-' + date2 + '.csv.data')
    set1 = set(dict(data1).keys())
    set2 = set(dict(data2).keys())
    print len(set1),len(set2),len(set1&set2)

def statistic2(date1,date2):
    data1 = getObj('./vehicle_appear_time/2016-03-'+date1+'.csv.data').items()
    data2 = getObj('./vehicle_appear_time/2016-03-' + date2 + '.csv.data').items()
    set1 = set(map(lambda x:x[0],filter(lambda x:x[1]>1,data1)))
    set2 = set(map(lambda x:x[0],filter(lambda x:x[1]>1,data2)))
    print len(set1),len(set2),len(set1&set2)

if __name__ == '__main__':
    statistic2('03','04')
    statistic('03','04')

    pass