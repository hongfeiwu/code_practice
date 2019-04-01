#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Queue
import threading
import time



"""

常用的 Queue 模块的属性:

queue(size): 创建一个大小为size的Queue对象。
qsize(): 返回队列的大小(由于在返回的时候，队列可能会被其它线程修改，所以这个值是近似值)
empty(): 如果队列为空返回 True，否则返回 False
full(): 如果队列已满返回 True，否则返回 False
put(item,block=0): 把item放到队列中，如果给了block(不为0)，函数会一直阻塞到队列中有空间为止
get(block=0): 从队列中取一个对象，如果给了 block(不为 0)，函数会一直阻塞到队列中有对象为止
"""
exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print "Starting " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name


def process_data(thread_name, q):
    while not exitFlag:
        queueLock.acquire()  # 占据锁
        if not workQueue.empty():
            data = q.get()
            queueLock.release()  # 释放锁
            print "%s processing %s" % (thread_name, data)
        else:
            queueLock.release()   # 占据锁
        time.sleep(1)


threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

# 创建新线程
for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"