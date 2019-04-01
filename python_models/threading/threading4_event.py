# -*- coding: UTF-8 -*-
from threading import Event,Thread
import threading

"""
事件用于在线程间通信。一个线程发出一个信号，其他一个或多个线程等待。
Event 通过通过 个内部标记来协调多线程运 。
法 wait() 阻塞线程执 ，直到标记为 True。 set() 将标记设为 True，clear() 更改标记为 False。isSet() 用于判断标记状态。


"""


def test_event():
    e = Event()

    def test():
        for i in range(5):
            print 'start wait'
            e.wait()
            e.clear()  # 如果不调用clear()，那么标记一直为 True，wait()就不会发生阻塞行为
            print i

    Thread(target=test).start()
    return e


ee = test_event()
