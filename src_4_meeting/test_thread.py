#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
import time

# 为线程定义一个函数
def print_time(threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )

# 创建两个线程
try:
   thread1 = thread.start_new_thread( print_time, ("Thread-1", 1) )
   thread2 = thread.start_new_thread( print_time, ("Thread-2", 1) )
except:
   print "Error: unable to start thread"

print thread1
exit(0)
threads = []
threads.append(thread1)
threads.append(thread2)

for t in threads:
   t.join()
