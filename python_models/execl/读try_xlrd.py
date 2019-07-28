# -*- coding: utf-8 -*-
"""

♦ 0. empty（空的）,1 string（text）, 2 number, 3 date, 4 boolean, 5 error， 6 blank（空白表格）
"""
import xlrd

xlsx_files = [u'/Users/whf/dev/code_practice/python_models/execl/students.xls']
for item_xlsx in xlsx_files:
    #  打开Excel文件读取数据
    data = xlrd.open_workbook(item_xlsx)

    # 获取一个工作表，会返回一个xlrd.sheet.Sheet()对象
    table = data.sheets()[0]    # 通过索引顺序获取

    print('table对象为{}'.format(table))
    # table = data.sheet_by_index(1)  # 通过索引顺序获取
    # table = data.sheet_by_name('Sh1')   # 通过名称获取
    # names = data.sheet_names()  # 返回book中所有工作表(sheet)的名字
    # print(names)
    # # data.sheet_loaded(sheet_name or indx)
    # # 检查某个sheet是否导入完毕
    # print(data.sheet_loaded('Sh1'))
    # print(data.sheet_loaded(1))

    # 行的操作
    nrows = table.nrows  # 获取该sheet中的有效行数
    print(nrows)

    for i in range(nrows):
        j = i + 1
        if j < nrows:
            string = str(table.row(j)[1].value)
            pass
    # print(table.row(2))  # 返回由该行中所有的单元格对象组成的列表
    # [number:1.0, text:'15330852404608', text:'吴茜', text:'0852', text:'工程硕士', text:'085208', text:'电子与通信工程', empty:'']
    # print(table.row_slice(7, start_colx=4, end_colx=None))   # 切片 返回由该行中start_colx开始至end_colx列的所有的单元格对象组成的列表
    # print(table.row_types(7, start_colx=0, end_colx=None))  # 返回由该行中所有单元格的数据类型组成的列表
    # print(table.row_values(7, start_colx=0, end_colx=None))  # 返回由该行中所有单元格的数据组成的列表
    # table.row_len(rowx)  # 返回该列的有效单元格长度

    # 列的操作
    # ncols = table.ncols  # 获取列表的有效列数
    # print(table.col(3, start_rowx=37, end_rowx=None))  # 返回由该列中start_rowx行至end_rowx行所有的单元格对象组成的列表
    # print(table.col_slice(3, start_rowx=38, end_rowx=None))  # 切片 返回由该列中start_rowx行至end_rowx行所有的单元格对象组成的列表
    # print(table.col_types(3, start_rowx=35, end_rowx=None))  # 返回由该列中start_rowx行至end_rowx行所有单元格的数据类型组成的列表
    # print(table.col_values(3, start_rowx=36, end_rowx=None))  # 返回由该列中start_rowx行至end_rowx行所有单元格的数据组成的列表
    # 单元格操作
    print(table.cell(4, 5))  # 返回单元格对象
    print(table.cell_type(7, 4))  # 返回单元格中的数据类型
    print(table.cell_value(7, 4))  # 返回单元格中的数据
    print(table.cell_xf_index(3, 4))  # 暂时还没有搞懂



