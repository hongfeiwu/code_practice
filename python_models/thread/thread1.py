#!/usr/bin/python
# -*- coding: UTF-8 -*-

import thread
from thread import _local
import time
from time import ctime

"""
Python 供了几个用于多线程编程的模块，包括 thread, threading 和 Queue 等。
thread 和 threading 模块允许程序员创建和管理线程。thread 模块 供了基本的线程和锁的支持，
而 threading 供了更高级别，功能更强的线程管理的功能。
Queue 模块允许用户创建一个可以用于多个线程之间 共享数据的队列数据结构。

Python解释器中可以同时运行多个线程，但是再任意时刻只能有一个线程在解释器运行。

Python虚拟机的访问是由全局解锁器（GIL）控制的，由GIL保证同时只有一个线程的运行。

执行方式如下：
1.设置GIL
2.切换进一个进程执行
3.执行下面操作中的一个
　　a.运行指定数量的字节码（操作系统中是由时钟控制的）
　　b.线程主动出让控制权
4.把线程设置为睡眠状态，即切换出线程
5.解锁GIL
6.重复以上步骤

注意：1.调用外部代码时（C/C++扩展的内置函数），GIL保持锁定，因为外部代码没有Python字节码.

　　　2.I/O密集型的Python程序要比计算密集型的程序更好的利用多线程。



函数	描述
start_new_thread(function,args)	产生新线程，指定函数和参数  核心函数
allocate_lock()	                分配一个LockType类型的锁对象
exit()	                        线程退出
LockType对象的方法
acquire()	        尝试获取对象对象
locked          	如果获取了返回True否则返回False
release()	        释放锁
"""


def print_time(thread_name, delay, count):
    print "%s: %s  %s \n" % (thread_name, time.ctime(time.time()), str(count))
    count = count
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s  %s" % (thread_name, time.ctime(time.time()), str(count))

try:
    thread.start_new_thread(print_time, ("Thread-1", 1, 0))
    time.sleep(1)
    thread.start_new_thread(print_time, ("Thread-2", 3, 0))
except:
    print "Error: unable to start thread"


while 1:
    pass
