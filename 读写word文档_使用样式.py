# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 17:16:28 2019

@author: Administrator
"""

from docx import Document
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE
import sys

data_path = 'd:/test/'

os.chdir(data_path)

doc = Document()

# 打印出所有的字体样式
styles = doc.styles
print("\n".join([s.name for s in styles if s.type == WD_STYLE_TYPE.PARAGRAPH]))


document = Document('d:/test/demo.docx')
for p in document.paragraphs:
    print(len(p.text))
    print(p.style.name)

# 用游程遍历段落
document = Document('d:/test/demo.docx')
for p in document.paragraphs:
    print('====')
    for r in p.runs:
        print(len(r.text))
