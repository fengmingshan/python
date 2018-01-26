# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:23:45 2018

@author: Administrator
"""
import pandas as pd   #导入pandas库
from datetime import datetime #导入时间格式datetime
from datetime import date #导入时间格式date
from datetime import timedelta #导入时间格式date


fadian=r'd:\2018年工作\2018年铁塔发电费用核对\fadian_2017-11.xls'
jieguo=r'd:\2018年工作\2018年铁塔发电费用核对\计算结果\本月发单清单.xls'

def open_xls(x):
    df_fadian=pd.read_excel(fadian,dtype =str,encoding='utf-8') #导入机房价格
    return df_fadian

def write_xls(x,sheet):
    writer = pd.ExcelWriter(jieguo) #输出到excel
    x.to_excel(writer, '%s_发单清单'%sheet)
    writer.save()
    return None

def main():  
    df_fadian=open_xls(fadian)
    col_name = list(df_fadian.columns)
    col_name.insert(col_name.index('站址来源（新建、存量）(不需填写）'),'当月发电次数')
    col_name.insert(col_name.index('铁塔审核发电开始时间'),'退服时长')
    col_name.insert(col_name.index('核减原因'),'剔除蓄电池保障3小时的时长')
    col_name.insert(col_name.index('发电日期'),'对应电信网管站址')
    col_name.insert(col_name.index('备注'),'发电是否及时')
    df_fadian=df_fadian.reindex(columns=col_name) 
    df_fadian['结算时长']=0
    df_fadian['结算次数']=0
    df_fadian['共享系数']=0
    df_fadian['油价']=0
    df_fadian['油费（不含税）']=0
    df_fadian['发电服务费（不含税）']=0
    df_fadian['总费用（不含税）']=0
    tmp=df_fadian['共享系数']   #使用tmp变流量取出'共享系数'一列
    df_fadian.drop(labels=['共享系数'], axis=1,inplace = True)  #原表中删除'共享系数'一列
    df_fadian.insert(45,'共享系数',tmp)     #将‘共享系数’列插回到原表第46列
    df_fadian.fillna('0',inplace = True)
    df_fadian['发电日期']=df_fadian['发电日期'].astype(date)
    df_fadian[['市电停电时间','系统发电开始时间','系统发电结束时间','铁塔审核发电开始时间','铁塔审核发电结束时间']]=\
    df_fadian[['市电停电时间','系统发电开始时间','系统发电结束时间','铁塔审核发电开始时间','铁塔审核发电结束时间']].astype(datetime)

    for i in range(0,len(df_fadian),1):
        if df_fadian[i,'市电停电时间']=Null:
            df_fadian['剔除蓄电池保障3小时的时长']=df_fadian['铁塔审核发电结束时间']-df_fadian['铁塔审核发电开始时间']
        elif :
            df_fadian['剔除蓄电池保障3小时的时长']=df_fadian['铁塔审核发电结束时间']-df_fadian['市电停电时间']
    
    sheet=df_fadian.iloc[1,13][:-12]    #从发电表取第14列第1行发电月份的2017-11，做为输出excel的sheet名称
    write_xls(df_fadian,sheet)




if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    

