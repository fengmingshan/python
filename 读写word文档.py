# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:07:52 2019

@author: Administrator
"""


from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
import os
from docx.shared import Pt

data_path = 'd:/test/'

os.chdir(data_path)

document = Document()

# 修改文档字体
document.styles['Normal'].font.name = u'华文楷体'
document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'华文楷体')
document.styles['Normal'].font.size = Pt(20)

# 添加标题 等级0
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
paragraph1 = document.add_paragraph('本周各县均无无新增基站', style= None)
document.add_paragraph('各县超闲基站分析', style='List Number')

paragraph1.style = document.styles['Normal']

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))

# 添加第二段
document.add_heading('二、4G流量', level=1)
paragraph2 = document.add_paragraph('本周4G流量较上周大幅度增长，增长较多的有宣威、会泽、富源；下降的有麒麟、沾益、马龙。', style = style_normal)
paragraph2.style = document.styles['Normal']

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))

# 添加第三段

document.add_heading('三、4G用户数', level=1)

paragraph3 = document.add_paragraph('本周4G用户数上周有所减少，增长的有宣威、会泽、富源；下降的有麒麟、沾益、马龙。', style = style_normal)
paragraph3.style = document.styles['Normal']

# 添加图片
document.add_picture('野性的呼唤.png', width=Inches(2.25))


document.add_page_break()

document.save('demo.docx')
