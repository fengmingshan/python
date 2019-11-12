# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-10-24 14:44:41
# @Last Modified by:   Administrator
# @Last Modified time: 2019-10-25 09:31:46

import pandas as pd
import os
import numpy as np
from openpyxl.styles import Alignment,Font
from openpyxl import Workbook, load_workbook

data_path = 'D:/Test/修改Excel表格样式'
os.chdir(data_path)
print('当前工作目录设置为{path}'.format(path = data_path))

wb = load_workbook('sample.xlsx')

ws = wb.get_sheet_by_name('全部基站详单')

for col in ws.columns:
    for cell in col:
        cell.alignment = Alignment(horizontal='general',
                                     vertical='bottom',
                                     text_rotation=0,
                                     wrap_text=True,
                                     shrink_to_fit=True,
                                     indent=0)
        cell.font = Font(name='Calibri',
                         size=11,
                         color='FF000000',
                         bold=False,
                         italic=False,
                         vertAlign=None,
                         underline='none',
                         strike=False)
wb.save("周报.xlsx")
