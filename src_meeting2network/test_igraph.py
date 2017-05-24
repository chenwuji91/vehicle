#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/20 16:47
# @Author  : chenwuji
# @File    : test_igraph.py
# @Software: PyCharm Community Edition
import igraph as gg

if __name__ == '__main__':
    g1 = gg.Graph()
    g1.add_vertices(3)
    g1.add_edges([(0, 1), (1, 2),(2,0),(2,1)])
    print g1
    pass