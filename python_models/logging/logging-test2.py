import os
import logging

"""
Configuration 配置方法
logging的配置大致有下面几种方式。

通过代码进行完整配置，参考开头的例子，主要是通过getLogger方法实现。
通过代码进行简单配置，下面有例子，主要是通过basicConfig方法实现。
通过配置文件，下面有例子，主要是通过 logging.config.fileConfig(filepath)

"""
filepath = os.path.join(os.path.dirname(__file__), 'logging-test2.conf')
logging.config.fileConfig(filepath)

aa = logging.getLogger()
