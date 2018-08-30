# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 09:15:25 2018

@author: Administrator
"""

import xlrd
import xlutils.copy
path = r'd:/test' + '//'
file = 'BSC设备巡检（日）.xls'

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
    
    
data =  '2018-08-30'
outSheet = outwb.get_sheet(0)
setOutCell(outSheet, 5, 8, '2018-08-30')
outwb.save(path + file.split('.')[0] + '_' + data +'.xls')