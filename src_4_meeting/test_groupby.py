#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/16 18:19
# @Author  : chenwuji
# @File    : test_groupby.py
# @Software: PyCharm Community Edition

from itertools import *
from operator import itemgetter


a = ['sa:a', 'a:b', 'a:bc', 'b:cd', 'a:bcde', 'a:bcde', 'a:b','sa:a', 'a:b', 'a:bc']
alist = map()
# print itemgetter(a)
# exit(0)
fun1 = lambda x:dict({x.split(':')[0]:x.split(':')[1]})
alist = map(fun1, a)
fun2 = lambda x:x[0]
for i, k in groupby(alist, key = fun2):
     print i, list(k)

if __name__ == '__main__':
    pass