# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 09:15:25 2018

@author: Administrator
"""

import xlrd
import xlutils.copy
import pandas as pd
path = r'd:/test' + '//'

file = '无线网数据配置（按需）_详细记录表.xls'
date_file = 'date_info.xlsx'
change_file = '基站数据配置.xlsx'

df_date = pd.read_excel(path + date_file, encoding = 'utf-8')
df_change =  pd.read_excel(path + change_file, encoding = 'utf-8')

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
i = 0
for date in date_list:
    date = str(date).split(' ')[0]
    outSheet = outwb.get_sheet(0)
    for j in range(0,30,1):
        setOutCell(outSheet, 0,2+j, df_change.loc[i*30+j,'ENODEBName'])
        setOutCell(outSheet, 1,2+j, '邻区优化')
        setOutCell(outSheet, 2,2+j,'-')
        setOutCell(outSheet, 3,2+j,'-')
        setOutCell(outSheet, 4,2+j,date)
    outwb.save(path + file.split('.')[0] + '_' + date +'.xls')