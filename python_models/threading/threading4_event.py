# -*- coding: UTF-8 -*-
from threading import Event,Thread
import threading

"""
事件用于在线程间通信。一个线程发出一个信号，其他一个或多个线程等待。
Event 通过通过 个内部标记来协调多线程运 。
法 wait() 阻塞线程执 ，直到标记为 True。 set() 将标记设为 True，clear() 更改标记为 False。isSet() 用于判断标记状态。


"""


import threading
import time


class WorkThread(threading.Thread):
    def __init__(self, signal):
        threading.Thread.__init__(self)
        self.singal = signal

    def run(self):
        print("妹纸 %s,睡觉了 ..." % self.name)
        self.singal.wait()
        print("妹纸 %s, 起床..." % self.name)

if __name__ == "__main__":

    singal = threading.Event()
    for t in range(0, 6):
        thread = WorkThread(singal)
        thread.start()

    print("三秒钟后叫妹纸起床 ")
    time.sleep(3)
    # 唤醒阻塞中的妹纸
    singal.set()
