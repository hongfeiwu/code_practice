# encoding=utf-8

import numpy as np


def main():
    list1 = [
        [1, 3, 5],
        [4, 6, 7]
    ]

    print type(list1)

    np_list = np.array(list1)   # 通过给array函数传递Python的序列对象创建np数组
    b = np.array((5, 6, 7, 8))
    print type(np_list)

    print "数组的大小可以通过其shape属性"
    print np_list.shape
    print b.shape
    print b.dtype           # 数组的元素类型可以通过dtype属性获得
                            # 通过dtype参数在创建时指定元素类型
    aa = np.array([[1, 2, 3, 4],[4, 5, 6, 7], [7, 8, 9, 10]], dtype=np.float)
    print aa.dtype, aa

    print "在保持数组元素个数不变的情况下，改变数组每个轴的长度"
    np_list.shape = 1, 6
    print np_list

    d = np_list.reshape((3, 2))  # 使用数组的reshape方法，可以创建一个改变了尺寸的新数组，
    print d                     # 原数组的shape保持不变


if __name__ == '__main__':
    main()
