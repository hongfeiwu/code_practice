#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time


"""
提供除了thread以及其他同步机制，主要是thread类
Threading模块下的thread类的使用:

函数	描述
run()	    通常需要重写，编写代码实现 做需要的功能。定义线程功能的函数
getName()	获得线程对象名称
setName()	设置线程对象名称
start()	    启动线程
jion([timeout])	等待另 一线程结束后再运行。timeout设置等待时间。
setDaemon(bool)	设置子线程是否随主线程一起结束，必须在start()之前调用。默认为False。
isDaemon()	    判断线程是否随主 线程一起结束。
isAlive()	    检查线程是否在运行中。
"""
exitFlag = 0


class MyThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def print_time(thread_name, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        counter -= 1


# 创建新线程
thread1 = MyThread(1, "Thread-1", 1)
thread2 = MyThread(2, "Thread-2", 2)

# 开启线程 start 启动线程
thread1.start()
thread2.start()

print "Exiting Main Thread"
