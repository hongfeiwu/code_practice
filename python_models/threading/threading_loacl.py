# -*- coding: utf-8 -*-
"""
threading-local对象最重要的就是它的数据对线程是局部的
用来保存一个全局变量，但是这个全局变量只有在当前线程才能访问

"""
import threading
from threading import local

global_num = 0
# l = threading.Lock()


def thread_cal():
    global global_num
    for i in xrange(1000):
        # l.acquire()
        # global_num += 1
        # l.release()
        # 执行函数时，global_num += 1 并不是一个原子操作，因此执行过程可能被其他线程中断，导致其他线程读到一个脏值,当global_num为局部变量时，不存在问题
        # 加锁可解决这个问题,
        global_num += 1

# Get 10 threads, run them and wait them all finished.
threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    # 执行线程
    threads[i].start()
for i in range(10):
    threads[i].join()

# Value of global variable can be confused.
print global_num

"""
解决办法1、
"""


mydata = local()
mydata.number = 42
print mydata.number     # 42
print mydata.__dict__        # {'number': 42}
mydata.__dict__.setdefault('widgets', [])

log = []


def f():
    items = mydata.__dict__.items()    # items = []
    items.sort()
    log.append(items)
    mydata.number = 11
    log.append(mydata.number)

thread = threading.Thread(target=f)
thread.start()
thread.join()
print log   # [[], 11]

# 在另一个线程里对数据的更改不会影响到当前线程里的数据
print mydata.number    # 42

