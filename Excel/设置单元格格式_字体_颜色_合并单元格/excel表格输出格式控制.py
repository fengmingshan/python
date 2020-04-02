# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:01:04 2019

@author: Administrator
"""

import pandas as pd
import numpy as np

df  = pd.DataFrame({'区县': ['富源', '会泽', '陆良', '罗平', '马龙', '麒麟', '师宗', '宣威', '沾益', '合计'],
                    '物理站址数量': np.random.randint(90, 400, size=10, dtype='int'),
                    '上周语音话务量': np.random.randint(15000, 45000, size=10, dtype='int'),
                    '本周语音话务量': np.random.randint(15000, 45000, size=10, dtype='int'),
                    '话务量环比变化': np.random.uniform(-0.1, 0.1, size=10),
                    '上周DO流量': np.random.randint(200, 4500, size=10, dtype='int'),
                    '本周DO流量': np.random.randint(200, 4500, size=10, dtype='int'),
                    'DO流量环比变化': np.random.uniform(-0.1, 0.1, size=10),
                    '本周DO在线用户数': np.random.randint(1000, 10000, size=10, dtype='int'),
                    '本周忙时登记用户数': np.random.randint(30000, 150000, size=10, dtype='int')
                    })

df['物理站址数量'] = df['物理站址数量'].astype(int)
df['上周语音话务量'] = df['上周语音话务量'].astype(int)
df['本周语音话务量'] = df['本周语音话务量'].astype(int)
df['上周DO流量'] = df['上周DO流量'].astype(int)
df['本周DO流量'] = df['本周DO流量'].astype(int)
df['本周DO在线用户数'] = df['本周DO在线用户数'].astype(int)
df['本周忙时登记用户数'] = df['本周忙时登记用户数'].astype(int)

df['话务量环比变化'] = df['话务量环比变化'].astype(float)
df['DO流量环比变化'] = df['DO流量环比变化'].astype(float)

with pd.ExcelWriter('3G话务周报示例.xlsx') as writer:
    workbook = writer.book
    # 1.设置单元格格式
    col_fmt = workbook.add_format({'bold': True,  # 字体加粗
                                   'font_size': 10,  # 字体大小
                                   'font_name': u'微软雅黑',  # 字体
                                   'num_format': '0.00',  # 数字格式
                                   'bg_color': '#574981',  # 单元格背景色
                                   'valign': 'vcenter',  # 垂直对齐方式
                                   'align': 'center',  # 水平对齐方式
                                   'top' : 2,  # 上边框，后面参数是线条宽度
                                   'left' : 2,  # 左边框
                                   'right' : 2,  # 右边框
                                   'bottom' : 2,  # 底边框
                                   'border' : 1 , # 边框
                                   'text_wrap': True})  # 自动换行，可在文本中加 '\n'来控制换行的位置
    noraml_fmt = workbook.add_format({"font_name": u"微软雅黑"})
    percent_fmt = workbook.add_format({'num_format': '0.00%'})
    header_fmt = workbook.add_format({'bold': True,
                                      'font_name': u'微软雅黑',
                                      'font_size': 16,  # 字体大小
                                      'align': 'center',  # 水平对齐方式
                                      'border' : 2 , # 边框
                                      'font_color': 'red',
                                      'valign': 'vcenter'}) #设置标题格式
    title_fmt = workbook.add_format({'bold': True,
                                    'font_name': u'微软雅黑',
                                    'align': 'center',  # 水平对齐方式
                                    'border' : 2 , # 边框
                                    'font_color': 'red',
                                    'valign': 'vcenter'}) #设置标题格式

    red_fmt = workbook.add_format({'bg_color': '#ff413b',
                                   'num_format': '0.00%'})
    border_format = workbook.add_format({'border' : 1 })

    # 2.将表格内容，写入到excel
    # 写入表格内容，不包含列名
    df.to_excel(
        writer,
        sheet_name=u'话务周报样例',
        encoding='utf8',
        header=False,
        index=False,
        startcol=0,
        startrow=3)

    worksheet1 = writer.sheets[u'话务周报样例']

    # 写入列名，格式设置为 col_fmt
    for col_num, value in enumerate(df.columns.values):
        worksheet1.write(2, col_num, value, col_fmt)

    # 3.单元格格式生效
    # worksheet1.write(row, col, data , fmt) # 带格式写入一个单元格
    # worksheet1.write_row('A1',data , fmt) # 带格式写入一整行
    # worksheet1.write_column('A1',data , fmt) # 带格式写入一整列
    # worksheet1.set_column('A:E', 15 , fmt) # 设置列宽及格式
    # worksheet1.set_row('A:E', 15 , fmt) # 设置行高及格式

    # 增加表格 header 和 title
    worksheet1.merge_range('A1:J1', u'全部基站话务量数据汇总', header_fmt)
    worksheet1.merge_range('C2:E2', u'语音话务量（erl）', title_fmt)
    worksheet1.merge_range('F2:H2', u'DO数据流量（GB）', title_fmt)

    l_end = len(df) + 3
    # 条件格式设置单元格格式：
    worksheet1.conditional_format(
        'A3:D%d' % l_end,
        {'type': 'no_blanks', 'format': noraml_fmt}) # 所有非空单元格设置为 noraml_fmt
    worksheet1.conditional_format(
        'F3:G%d' % l_end,
        {'type': 'no_blanks', 'format': noraml_fmt})
    worksheet1.conditional_format(
        'I3:J%d' % l_end,
        {'type': 'no_blanks', 'format': noraml_fmt})
    worksheet1.conditional_format(
        'E3:E%d'% l_end,
        {'type': 'no_blanks', 'format': percent_fmt}) # 话务量环比变化，设置为 percent_fmt
    worksheet1.conditional_format(
        'H3:H%d'% l_end,
        {'type': 'no_blanks', 'format': percent_fmt}) # DO流量环比变化，设置为 percent_fmt

    # 条件格式：对 话务量环比变化小于0的单元格显示红色
    worksheet1.conditional_format(
        'E3:E%d'% l_end,
        {'type': 'cell', 'criteria': '<', 'value': 0, 'format': red_fmt})
    # 条件格式：对 DO流量环比变化小于0的单元格显示红色
    worksheet1.conditional_format(
        'H3:H%d'% l_end,
        {'type': 'cell', 'criteria': '<', 'value': 0, 'format': red_fmt})

    # 设置列宽
    worksheet1.set_column('A:J', 10)

    # 加边框
    worksheet1.conditional_format('A4:J%d' % l_end, {'type': 'no_blanks', 'format': border_format})
    worksheet1.conditional_format('A2:B2', {'type': 'blanks', 'format': title_fmt})
    worksheet1.conditional_format('I2:J2', {'type': 'blanks', 'format': title_fmt})


# =============================================================================
# 数字格式示例
# =============================================================================
# format1.set_num_format('dd mm yyyy')  # Format string.
# worksheet.write(1, 0, 2019-11-12, format1)       # -> 12 11 2019

# format2.set_num_format(0x0F)          # Format index.
# worksheet.write(1, 1, 17, format2)       # -> 0x11

# format01.set_num_format('0.000')
# worksheet.write(1, 0, 3.1415926, format01)       # -> 3.142

# format02.set_num_format('#,##0')
# worksheet.write(2, 0, 1234.56, format02)         # -> 1,235

# format03.set_num_format('#,##0.00')
# worksheet.write(3, 0, 1234.56, format03)         # -> 1,234.56

# format04.set_num_format('0.00')
# worksheet.write(4, 0, 49.99, format04)           # -> 49.99

# format05.set_num_format('mm/dd/yy')
# worksheet.write(5, 0, 36892.521, format05)       # -> 01/01/01

#format06.set_num_format('mmm d yyyy')
# worksheet.write(6, 0, 36892.521, format06)       # -> Jan 1 2001

#format07.set_num_format('d mmmm yyyy')
# worksheet.write(7, 0, 36892.521, format07)       # -> 1 January 2001

#format08.set_num_format('dd/mm/yyyy hh:mm AM/PM')
# worksheet.write(8, 0, 36892.521, format08)      # -> 01/01/2001 12:30 AM

#format09.set_num_format('0 "dollar and" .00 "cents"')
# worksheet.write(9, 0, 1.87, format09)           # -> 1 dollar and .87 cents
