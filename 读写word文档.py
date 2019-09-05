# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:07:52 2019

@author: Administrator
"""


from docx import Document
from docx.shared import Inches

data_path = 'd:/test/'

os.chdir(data_path)

document = Document()

# 添加段落
document.add_heading('4G话务周报', level=0)

#p = document.add_paragraph('4G话务周报划小到支局 ')
#p.add_run('bold').bold = True
#p.add_run(' and some ')
#p.add_run('italic.').italic = True

# 添加第一段
document.add_heading('一、基站数量', level=1)

# document.add_paragraph(
#    'first item in unordered list', style='List Bullet'
#)

# 添加小节
document.add_paragraph('各县基站数量分析', style='List Number')

document.add_paragraph('本周各县均无无新增基站', style=None)

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))

# 添加第二段
document.add_heading('二、4G流量', level=1)

document.add_paragraph('本周4G流量较上周大幅度增长，增长较多的有宣威、会泽、富源；下降的有麒麟、沾益、马龙。', style=None)

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))

# 添加第三段

document.add_heading('三、4G用户数', level=1)

document.add_paragraph('本周4G4G用户数上周有所减少，增长的有宣威、会泽、富源；下降的有麒麟、沾益、马龙。', style=None)

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))


# 添加表格
# records = (
#    (3, '101', 'Spam'),
#    (7, '422', 'Eggs'),
#    (4, '631', 'Spam, spam, eggs, and spam')
#)
#
#table = document.add_table(rows=1, cols=3)
#hdr_cells = table.rows[0].cells
#hdr_cells[0].text = 'Qty'
#hdr_cells[1].text = 'Id'
#hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#    row_cells = table.add_row().cells
#    row_cells[0].text = str(qty)
#    row_cells[1].text = id
#    row_cells[2].text = desc

document.add_page_break()

document.save('demo.docx')
