#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Python 提供了两个级别访问的网络服务。：

低级别的网络服务支持基本的 Socket，它提供了标准的 BSD Sockets API，可以访问底层操作系统Socket接口的全部方法。
高级别的网络服务模块 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。

TCP服务端：

1 创建套接字，绑定套接字到本地IP与端口
   # socket.socket(socket.AF_INET,socket.SOCK_STREAM) , s.bind()
2 开始监听连接                   #s.listen()
3 进入循环，不断接受客户端的连接请求              #s.accept()
4 然后接收传来的数据，并发送给对方数据         #s.recv() , s.sendall()
5 传输完毕后，关闭套接字                     #s.close()

socket.socket([family[, type[, proto]]])
    family: 套接字家族可以使AF_UNIX或者AF_INET
    type: 套接字类型可以根据是面向连接的还是非连接分为SOCK_STREAM或SOCK_DGRAM
    protocol: 一般不填默认为0.

服务端
s.bind()	绑定地址（host,port）到套接字， 在AF_INET下,以元组（host,port）的形式表示地址。
s.listen()	开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。
s.accept()	被动接受TCP客户端连接,(阻塞式)等待连接的到来
"""
import socket

ip_port = ('127.0.0.1', 9999)

sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print 'server waiting...'
    conn, addr = sk.accept()

    client_data = conn.recv(1024)
    print client_data
    conn.sendall('不要回答,不要回答,不要回答')

    conn.close()
