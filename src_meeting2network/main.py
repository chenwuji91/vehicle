#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 14:06
# @Author  : chenwuji
# @File    : main.py
# @Software: PyCharm Community Edition
# @Description: 读取可以碰面的pair  构建网络

import cPickle as p
import glob
import matplotlib.pyplot as plt


def getObj(path):
    dataFile = file(path,'r')
    obj = p.load(dataFile)
    return obj

def generate_network(filename = '2016-03-05 06_27_22.set.data'):
    pair_set = getObj(filename)
    __output_as_nx(pair_set)


def __output_as_nx(all_edge):
    import networkx as nx  # 导入NetworkX包
    G = nx.Graph()  # 建立一个空的无向图G
    for eachpair in all_edge:
        G.add_edge(eachpair[0],eachpair[1])


    counti = 0
    for i in nx.connected_component_subgraphs(G):
        counti +=1
        print counti
    comp  = nx.connected_components(G)
    clus = nx.clustering(G)

    print comp
    print clus

    # nx.
    # comp = nx.connected_components(G)
    #
    # comp_list = nx.connected_component_subgraphs(G)
    # counti = 0
    # for i in comp_list:
    #
    #     counti +=1
    #     print counti
    nx.draw(G,pos=nx.random_layout(G),node_size = 5,)  # 绘制网络G
    plt.savefig("ba.png")  # 输出方式1: 将图像存为一个png格式的图片文件
    plt.show()


if __name__ == '__main__':
    flist = glob.glob('../connection/*')
    for eachfile in flist:
        generate_network(eachfile)

    pass