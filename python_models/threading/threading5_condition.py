# -*- coding: UTF-8 -*-
from threading import Condition, current_thread, Thread
from time import sleep


"""
条件变量和 Lock 参数一样，是一个同步原语，当需要线程关注特定的状态变化或事件的发生时使用这个锁定。
可以认为，除了Lock带有的锁定池外，Condition还包含一个等待池，池中的线程处于状态图中的等待阻塞状态，
直到另一个线程调用notify()/notifyAll()通知；得到通知后线程进入锁定池等待锁定。

acquire([timeout])/release(): 调用关联的锁的相应方法。

wait([timeout]): 调用这个方法将使线程进入Condition的等待池等待通知，并释放锁。使用前线程必须已获得锁定，否则将抛出异常。

notify(): 调用这个方法将从等待池挑选一个线程并通知，收到通知的线程将自动调用acquire()尝试获得锁定（进入锁定池）；其他线程仍然在等待池中。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。

notifyAll(): 调用这个方法将通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定。调用这个方法不会释放锁定。使用前线程必须已获得锁定，否则将抛出异常。
"""

con = Condition()


def tc1():
    with con:
        for i in range(5):
            print current_thread().name, i
            sleep(0.3)
            if i == 3:
                con.wait()


def tc2():
    with con:
        for i in range(5):
            print current_thread().name, i
            sleep(0.1)
            con.notify()

Thread(target=tc1).start()
Thread(target=tc2).start()
