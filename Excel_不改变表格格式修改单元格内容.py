# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 09:15:25 2018

@author: Administrator
"""

import xlrd
import xlutils.copy
import pandas as pd
path = r'd:/test' + '//'

file = '无线网数据配置（按需）.xls'
date_file = 'date_info.xlsx'

df_date = pd.read_excel(path + date_file, encoding = 'utf-8')

newwb = xlrd.open_workbook(path + file , formatting_info=True)  # formatting_info 带格式导入
outwb = xlutils.copy.copy(newwb)                           # 建立一个副本来用xlwt来写
 
# 修改值
 
def setOutCell(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
    def _getOutCell(outSheet, colIndex, rowIndex):
    	""" HACK: Extract the internal xlwt cell representation. """
    	row = outSheet._Worksheet__rows.get(rowIndex)
    	if not row: return None
 
    	cell = row._Row__cells.get(colIndex)
    	return cell
 
	# HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I
 
    outSheet.write(row, col, value)
 
    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx
    # END HACK

date_list =list(df_date['日期']) 
for date in date_list:
    date = str(date).split(' ')[0]
    outSheet = outwb.get_sheet(0)
    setOutCell(outSheet, 6, 7, date)
    outwb.save(path + file.split('.')[0] + '_' + date +'.xls')