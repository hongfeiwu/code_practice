# -*- coding: UTF-8 -*-
from time import sleep
from threading import current_thread, Thread
import threading


"""
RLock 可重入锁是一个类似于Lock对象的同步原语，但同一个线程可以多次调用。

Lock 不支持递归加锁，也就是说即便在同 线程中，也必须等待锁释放。
通常建议改 RLock， 它会处理 "owning thread" 和 "recursion level" 状态，对于同 线程的多次请求锁 为，只累加
计数器。每次调 release() 将递减该计数器，直到 0 时释放锁，因此 acquire() 和 release() 必须 要成对出现。


Lock跟Rlock区别：RLock允许在同一线程中被多次acquire。而Lock却不允许这种情况
RLock对Lock进行了封装，增加了__enter__（acquire）,__exit__（release）的上下文管理器，所以需要用with语句
"""
lock = threading.RLock()


def show():
    with lock:
        print current_thread().name, i
        sleep(0.1)


def test():
    with lock:
        for i in range(3):
            show(i)

for i in range(2):
    Thread(target=test).start()
