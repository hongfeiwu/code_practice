w# -*- coding: utf-8 -*-
import mysql.connector
import random


def save(num):
    # 详细mysql语句用法详见http://www.cnblogs.com/zhangzhu/archive/2013/07/04/3172486.html
    # 打开数据库连接
    conn = mysql.connector.connect(host='localhost', user='root', password='openerp', database='whf_test')
    # 使用cursor()方法创建一个cursor对象，来管理查询
    cur = conn.cursor()
    # 使用execute()方法执行SQL，如果存在则删除
    cur.execute("drop table if exists act_code")
    # 使用预处理创建表
    cur.execute(" create table act_code ("
                "id int(1) auto_increment primary key,"
                "code varchar(10)"
                ")")
    for i in range(num):
        choiceCode = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
        # 随机生成10个数字
        code = [random.choice(choiceCode) for i in range(10)]
        code = ''.join(code)
        sql = 'insert into act_code (code) values(%s)'
        try:
            cur.execute(sql, [code])
            print code
        except BaseException as e:
            print(e)
            break

    # 提交并关闭连接
    conn.commit()
    cur.close()
    conn.close()
    print('完成')

if __name__ == '__main__':
    save(200)
