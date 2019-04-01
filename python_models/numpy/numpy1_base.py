# -*- coding: utf-8 -*-

"""
NumPy 的主要操作对象是同类型的多维数组。
它是一个由正整数元组索引，元素类型相同的表（通常元素是数字）。
在 NumPy 维度被称为 axes, axes 的数量称为 rank。

Numpy的数组类是ndarray
    ndarray.ndim        数组的 axes （维数）数值大小
    ndarray.shape       数组的维数   shape 是 (n, m)
    ndarray.size        数组元素的个数总和 size = n * m
    ndarray.dtype       数组中描述元素类型的一个对
        numpy.int32
        numpy.int16
        numpy.float64
        ……
    ndarray.itemsize    数组中每个元素所占字节数
        float64 的 itemsize 是 8 ( = 64/8bit)
        complex32 的 itemsize 是 4 ( = 32/8bit)
        ......
    ndarray.data        数组实际元素的缓存区
"""

import numpy as np

a = np.arange(15).reshape(3, 5)
print a
"""
array([[ 0,  1,  2,  3,  4],
       [ 5,  6,  7,  8,  9],
       [10, 11, 12, 13, 14]])
"""
a.shape   # （3， 5）
a.ndim      # 2
a.dtype.name    #  'int64'
a.itemsize      # 8
a.size      # 15
type(a)         # <type 'numpy.ndarray'>
b = np.array([6, 7, 8])
b        # array([6, 7, 8])
type(b)         # <type 'numpy.ndarray'>


# 创建数组
a = np.array([2, 3, 4])
b = np.array([1.2, 3.5, 5.1])
b = np.array([(1.5, 2, 3), (4, 5, 6)])      # array 将序列转化成高维数组
c = np.array([[1, 2], [3, 4]], dtype=complex)  # 数组的类型也能够在创建时具体指定
"""
zeros：用来创建元素全部是0的数组
ones：用来创建元素全部是1的数组
empty：用来创建未初始化的数据，因此是内容是不确定的，默认创建数组的类型是 float64。
arange：通过指定范围和步长来创建数组
linespace：通过指定范围和元素数量来创建数组
random：用来生成随机数
>>> np.zeros( (3,4) )
array([[ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  0.]])
>>> np.ones( (2,3,4), dtype=np.int16 )                # dtype can also be specified
array([[[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]],
       [[ 1, 1, 1, 1],
        [ 1, 1, 1, 1],
        [ 1, 1, 1, 1]]], dtype=int16)
>>> np.empty( (2,3) )                                 # uninitialized, output may vary
array([[  3.73603959e-262,   6.02658058e-154,   6.55490914e-260],
       [  5.30498948e-313,   3.14673309e-307,   1.00000000e+000]])

创建数字序列，NumPy 提供了一个和 range 相似的函数，可以返回一个数组而不是列表。
>>> np.arange( 10, 30, 5 )
array([10, 15, 20, 25])
>>> np.arange( 0, 2, 0.3 )                 # it accepts float arguments
array([ 0. ,  0.3,  0.6,  0.9,  1.2,  1.5,  1.8])
当 arange 的参数是浮点型的，由于有限的浮点精度，通常不太可能去预测获得元素的数量。
出于这个原因，通常选择更好的函数 linspace
In [7]: np.linspace( 0, 2, 9 )
Out[7]: array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ,  1.25,  1.5 ,  1.75,  2.  ])


打印数组时，NumPy 显示出来和嵌套的列表相似，但是具有以下布局：
    最后一个 axis 从左到右打印，
    第二到最后一个从上到下打印，
    剩余的也是从上到下打印，每一片通过一个空行隔开。
In [8]: a = np.arange(6)
In [9]: a
Out[9]: array([0, 1, 2, 3, 4, 5])

In [10]: b = np.arange(12).reshape(4,3)
In [11]: b
Out[11]:
array([[ 0,  1,  2],
       [ 3,  4,  5],
       [ 6,  7,  8],
       [ 9, 10, 11]])
一个数组太大而不能被打印，那么 NumPy 会自动忽略中间的只打印角上的数据
强制 NumPy 去打印整个数组，你可以通过 set_printoptions 改变打印选项。
"""













