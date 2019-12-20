# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:01:04 2019

@author: Administrator
"""

import pandas as pd



with pd.ExcelWriter('修改excel表格样式示例.xlsx') as writer:
    workbook = writer.book
    # 1.设置单元格格式
    col_fmt = workbook.add_format({'bold': True, # 字体加粗
                                     'font_size': 10, # 字体大小
                                     'font_name': u'微软雅黑', # 字体
                                     'num_format': 'yyyy-mm-dd', # 数字格式
                                     'bg_color': '#574981', # 单元格背景色
                                     'valign': 'vcenter', # 垂直对齐方式
                                     'align': 'center', # 水平对齐方式
                                     'top':2, # 上边框，后面参数是线条宽度
                                     'left':2, # 左边框
                                     'right':2, # 右边框
                                     'bottom':2, # 底边框
                                     'text_wrap': True}) # 自动换行，可在文本中加 '\n'来控制换行的位置
    # 数字格式
    num_fmt = workbook.add_format()
    num_fmt.set_num_format(0x0F)
    # 2.将表格内容，写入到excel
    l_end = len(df) + 3
    df.to_excel(
        writer,
        sheet_name=u'测试页',
        encoding='utf8',
        header=False,
        index=False,
        startcol=0,
        startrow=3)
    worksheet1 = writer.sheets[u'测试页']
    for col_num, value in enumerate(df.columns.values):
        worksheet1.write(2, col_num, value, col_fmt)

    # 3.单元格格式生效
    # worksheet1.write(row, col, data , fmt) # 带格式写入一个单元格
    # worksheet1.write_row(“A1”,data , fmt) # 带格式写入一整行
    # worksheet1.write_column(“A1”,data , fmt) # 带格式写入一整列
    # worksheet1.set_column('A:E', 15 , fmt) # 设置列宽及格式
    # worksheet1.set_row('A:E', 15 , fmt) # 设置行高及格式

    # 增加表格说明
    worksheet1.merge_range('A1:J1', u'全部基站话务量数据汇总', note_fmt)
    worksheet1.merge_range('C2:E2', u'语音话务量（erl）', note_fmt)
    worksheet1.merge_range('F2:H2', u'DO数据流量（GB）', note_fmt)
    # 设置列宽
    worksheet1.set_column('A:E', 15, fmt)
    # 有条件设定表格格式：金额列
    worksheet1.conditional_format(
        'B3:E%d' %
        l_end, {
            'type': 'cell', 'criteria': '>=', 'value': 1, 'format': amt_fmt})
    # 有条件设定表格格式：百分比
    worksheet1.conditional_format(
        'E3:E%d' %
        l_end, {
            'type': 'cell', 'criteria': '<=', 'value': 0.1, 'format': percent_fmt})
    # 条件格式：小于-4%的单元格显示红色
    worksheet1.conditional_format(
        'E3:E%d' %
        l_end, {
            'type': 'cell', 'criteria': '<', 'value': -0.04, 'format': red_fmt})
    # 加边框
    worksheet1.conditional_format('A1:J%d' % l_end, {'type': 'no_blanks', 'format': border_format})
    worksheet1.conditional_format('A2:J2', {'type': 'no_blanks', 'format': border_format})

# =============================================================================
# 数字格式示例
# =============================================================================
#format1.set_num_format('dd mm yyyy')  # Format string.
# worksheet.write(1, 0, 2019-11-12, format1)       # -> 3.142

#format2.set_num_format(0x0F)          # Format index.
# worksheet.write(1, 1, 17, format2)       # -> 3.142

#format01.set_num_format('0.000')
#worksheet.write(1, 0, 3.1415926, format01)       # -> 3.142

#format02.set_num_format('#,##0')
#worksheet.write(2, 0, 1234.56, format02)         # -> 1,235

#format03.set_num_format('#,##0.00')
#worksheet.write(3, 0, 1234.56, format03)         # -> 1,234.56

#format04.set_num_format('0.00')
#worksheet.write(4, 0, 49.99, format04)           # -> 49.99

#format05.set_num_format('mm/dd/yy')
#worksheet.write(5, 0, 36892.521, format05)       # -> 01/01/01

#format06.set_num_format('mmm d yyyy')
#worksheet.write(6, 0, 36892.521, format06)       # -> Jan 1 2001

#format07.set_num_format('d mmmm yyyy')
#worksheet.write(7, 0, 36892.521, format07)       # -> 1 January 2001

#format08.set_num_format('dd/mm/yyyy hh:mm AM/PM')
#worksheet.write(8, 0, 36892.521, format08)      # -> 01/01/2001 12:30 AM

#format09.set_num_format('0 "dollar and" .00 "cents"')
#worksheet.write(9, 0, 1.87, format09)           # -> 1 dollar and .87 cents