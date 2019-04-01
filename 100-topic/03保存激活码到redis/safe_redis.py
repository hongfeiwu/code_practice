#!/usr/bin/env python
# coding: utf-8
import redis
import random

HOST = 'localhost'
PORT = 6379

# 连接到数据库
r = redis.Redis(HOST, PORT)
# redis 安装http://www.cnblogs.com/moon521/p/5301895.html

def save(num):
    for i in range(num):
        choiceCode = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
        code = [str(i) + random.choice(choiceCode) for i in range(10)]
        code = ''.join(code)
        # 将生成的激活码存入数据库中
        r.sadd("code", code)
        print code


if __name__ == '__main__':
    save(200)
