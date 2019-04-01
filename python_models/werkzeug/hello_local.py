# -*- coding: utf-8 -*-

"""
在local模块中，Werkzeug实现了类似Python标准库中thread.local的功能。
用来保存一个全局变量，但是这个全局变量只有在当前线程才能访问
thread.local是线程局部变量，也就是每个线程的私有变量，具有线程隔离性，
可以通过线程安全的方式获取或者改变线程中的变量。
Local   LocalManager会确保不管是协程还是线程，只要当前请求处理完成之后清除Local中对应的内
LocalStack   在本协程（线程）中管理数据的方式是采用栈(操作_local.__storage__.[local._ident_func__()][‘stack’]这个list来模拟栈的操作)的方式
    可LocalManager对象强制释放,通常使用pop弹出，只保留当前使用的变量
            将一个Local对象作为自己的属性_local
            push、pop、top等方法或属性，调用这些属性或者方法时，该类会根据当前线程或协程的标识数值，在Local实例中对相应的数值进行操作。
LocalProxy       Local对象的一个代理
LocalManager       通过一个list类型的属性locals来存储所管理的Local或者LocalStack对象，还提供cleanup方法来释放所有的Local对象
"""

import threading
from threading import current_thread,local
from werkzeug.local import Local
l = Local()
l.__storage__


def add_arg(arg, i):
    l.__setattr__(arg, i)


for i in range(3):
    arg = 'arg' + str(i)
    t = threading.Thread(target=add_arg, args=(arg, i))
    t.start()

l.__storage__

"""
LocalStack LocalStack类和Local类类似，但是它实现了栈数据结构。
"""

from werkzeug.local import LocalStack, LocalProxy
import logging, random, threading, time
# 定义logging配置
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
_stack = LocalStack()
# 定义一个RequestConetxt类，它包含一个上下文环境。
# 当调用这个类的实例时，它会将这个上下文对象放入
# _stack栈中去。当退出该上下文环境时，栈会pop其中
# 的上下文对象。


class RequestConetxt(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __enter__(self):
        _stack.push(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            _stack.pop()

    def __repr__(self):
        return '%s, %s, %s' % (self.a, self.b, self.c)
# 定义一个可供不同线程调用的方法。当不同线程调用该
# 方法时，首先会生成一个RequestConetxt实例，并在这
# 个上下文环境中先将该线程休眠一定时间，之后打印出
# 目前_stack中的信息，以及当前线程中的变量信息。
# 以上过程会循环两次。


def worker(i):
    with request_context(i):
        for j in range(2):
            pause = random.random()
            logging.debug('Sleeping %0.02f', pause)
            time.sleep(pause)
            logging.debug('stack: %s' % _stack._local.__storage__.items())
            logging.debug('ident_func(): %d' % _stack.__ident_func__())
            logging.debug('a=%s; b=%s; c=%s' %
                          (LocalProxy(lambda: _stack.top.a),
                           LocalProxy(lambda: _stack.top.b),
                           LocalProxy(lambda: _stack.top.c)))
    logging.debug('Done')
# 调用该函数生成一个RequestConetxt对象


def request_context(i):
    i = str(i+1)
    return RequestConetxt('a'+i, 'b'+i, 'c'+i)
# 在程序最开始显示_stack的最初状态
logging.debug('Stack Initial State: %s' % _stack._local.__storage__.items())
# 产生两个线程，分别调用worker函数

for i in range(2):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
main_thread = threading.currentThread()

for t in threading.enumerate():
    if t is not main_thread:
        t.join()
# 在程序最后显示_stack的最终状态
logging.debug('Stack Finally State: %s' % _stack._local.__storage__.items())

