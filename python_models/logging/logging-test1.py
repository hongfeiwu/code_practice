# -*- coding: utf-8 -*-

import logging
import sys

"""
记录器（Logger）     记录器是开发者经常交互的对象
日志记录      日志记录是 logging 模块用来满足所有需求信息的包，包含了需要记录日志的地方、变化的字符串、参数、请求的信息队列等信息。
处理器     处理器将日志记录发送给其他输出终端，他们获取日志记录并用相关函数中处理它们。
    多种文件处理器（TimeRotated, SizeRotated, Watched），可以写入文件中
        StreamHandler 输出目标流比如 stdout 或 stderr
        SMTPHandler 通过 email 发送日志记录
        SocketHandler 将日志文件发送到流套接字
        SyslogHandler、NTEventHandler、HTTPHandler及MemoryHandler等
格式器     格式器负责将丰富的元数据日志记录转换为字符串，如果什么都没有提供，将会有个默认的格式器。
过滤器     过滤器允许对应该发送的日志记录进行细粒度控制。
记录器层级

"""

# 获取logger实例，如果参数为空则返回root logger
# getLogger()方法是最基本的入口，该方法参数可以为空，默认的logger名称是root
# 如果在同一个程序中一直都使用同名的logger，其实会拿到同一个实例，使用这个技巧就可以跨模块调用同样的logger来记录日志。
logger = logging.getLogger("AppName")

# 指定logger输出格式
"""
Formatter对象定义了log信息的结构和内容，构造时需要带两个参数：
一个是格式化的模板fmt，默认会包含最基本的level和 message信息
一个是格式化的时间样式datefmt，默认为 2003-07-08 16:49:45,896 (%Y-%m-%d %H:%M:%S)
"""
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')


# Handler 日志处理器 Handler用于向不同的输出端打log。
# 文件日志
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器, 处理器将日志记录发送给其他输出终端，他们获取日志记录并用相关函数中处理它们
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)

# 输出不同级别的log
# SetLevel 日志级别
# Logging有如下级别: DEBUG，INFO，WARNING，ERROR，CRITICAL
# 默认级别是WARNING，logging模块只会输出指定level以上的log。
# 这样的好处, 就是在项目开发时debug用的log，在产品release阶段不用一一注释，只需要调整logger的级别就可以了，很方便。
logger.debug('this is debug info')
logger.info('this is information')
logger.warn('this is warning message')
logger.error('this is error message')
logger.fatal('this is fatal message, it is same as logger.critical')
logger.critical('this is critical message')

"""
test.log内容
2018-03-14 14:25:46,129 INFO    : this is information
2018-03-14 14:25:46,129 WARNING : this is warning message
2018-03-14 14:25:46,129 ERROR   : this is error message
2018-03-14 14:25:46,129 CRITICAL: this is fatal message, it is same as logger.critical
2018-03-14 14:25:46,130 CRITICAL: this is critical message
"""

# 格式化输出
service_name = "Booking"
logger.error('%s service is down!' % service_name)  # 使用python自带的字符串格式化，不推荐
logger.error('%s service is down!', service_name)  # 使用logger的格式化，推荐
logger.error('%s service is %s!', service_name, 'down')  # 多参数格式化
logger.error('{} service is {}'.format(service_name, 'down'))  # 使用format函数，推荐

# 记录异常信息
try:
    1 / 0
except:
    # 等同于error级别，但是会额外记录当前抛出的异常堆栈信息
    logger.exception('this is an exception message')


# 移除一些日志处理器
logger.removeHandler(file_handler)