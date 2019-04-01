#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
TCP客户端:

1 创建套接字，连接远端地址
       # socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.connect()
2 连接后发送数据和接收数据          # s.sendall(), s.recv()
3 传输完毕后，关闭套接字          #s.close()



客户端
s.connect()	主动初始化TCP服务器连接，。一般address的格式为元组（hostname,port），如果连接出错，返回socket.error错误。
s.connect_ex()	connect()函数的扩展版本,出错时返回出错码,而不是抛出异常
"""
import socket
ip_port = ('127.0.0.1', 9999)

sk = socket.socket()
sk.connect(ip_port)

sk.sendall('请求占领地球')
# 1024代表最大接受量为1024字节，utf-8时一个中文字符占3个字段
server_reply = sk.recv(1024)
print server_reply

sk.close()