#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/16 15:31
# @Author  : chenwuji
# @File    : test_thread2.py
# @Software: PyCharm Community Edition

import thread
from time import sleep,ctime

loops = [4,2]

def loop(nloop, nsec, lock):
    sleep(nsec)
    print 'loop',nloop,ctime()
    lock.release()
def main():
    locks = []
    nloop = range(len(loops))

    for i in nloop:
        lock = thread.allocate_lock()
        lock.acquire()
        locks.append(lock)
    for i in nloop:
        thread.start_new_thread(loop,(i,loops[i],locks[i]))
    for i in nloop:
        while locks[i].locked():pass
    print 'all Done'

if __name__ == '__main__':
    main()
    pass