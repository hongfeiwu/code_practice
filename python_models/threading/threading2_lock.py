#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time

"""
原语锁定是一个同步原语，状态是锁定或未锁定。两个方法acquire()和release() 用于加锁和释放锁。

"""


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()


def print_time(thread_name, delay, counter):
    while counter:
        time.sleep(delay)
        print "%s: %s" % (thread_name, time.ctime(time.time()))
        counter -= 1


threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"



def show(num):
    print threading.current_thread().getName(), num

def thread_cal():
    local_num = 0
    for _ in xrange(1000):
        local_num += 1
    show(local_num)


threads = []
for i in range(10):
    threads.append(threading.Thread(target=thread_cal))
    threads[i].start()