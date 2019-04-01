#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string


def activation_code(id, length=10):
    """
    id + L + 随机码
    string模块中的3个函数：string.letters，string.printable，string.printable
    hex()将整数转换成16进制字符串
    """
    prefix = hex(int(id))[2:] + 'L'
    length = length - len(prefix)
    chars=string.ascii_letters+string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])


def get_id(code):
    """
    Hex to Dec
    """
    return str(int(code.upper(), 16))

if __name__ == "__main__":
    for i in range(1, 201):
        code = activation_code(i)
        id_hex = code.split('L')[0]
        id = get_id(id_hex)
        print code, id
