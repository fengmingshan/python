# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:23:45 2018

@author: Administrator
"""
import pandas as pd   #导入pandas库

fadian=r'd:\2018年工作\2018年铁塔发电费用核对\fadian_2017-11.xls'
def open_xls(x):
    df_fadian=pd.read_excel(fadian,dtype =str,encoding='utf-8') #导入机房价格
    return df_fadian

def main():  
    df_fadian=open_xls(fadian)
    col_name = list(df_fadian.columns)
    col_name.insert(col_name.index('退服开始时间'),'退服时长')
    col_name.insert(col_name.index('核减原因'),'剔除蓄电池保障3小时的时长')
    col_name.insert(col_name.index('发电日期'),'对应电信网管站址')
    df_fadian.reindex(columns=col_name) 



if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    

