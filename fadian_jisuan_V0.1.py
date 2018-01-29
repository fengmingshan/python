# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:23:45 2018

@author: Administrator
"""
import pandas as pd   #导入pandas库
from sqlalchemy import create_engine 
from datetime import datetime #导入时间格式datetime
from datetime import date #导入时间格式date
from datetime import timedelta #导入时间格式date
import datetime

engine=create_engine('mysql+pymysql://root:123456@218.63.75.42:3306/铁塔租费?charset=utf8',echo=False)
fadian=r'd:\2018年工作\2018年铁塔发电费用核对\fadian_2017-11.xls'
jieguo=r'd:\2018年工作\2018年铁塔发电费用核对\计算结果\本月发单清单.xls'
zhanzhi=r'd:\2018年工作\2018年铁塔发电费用核对\zhanzhi.xls'
zhangdan=r'd:\2018年工作\2018年铁塔发电费用核对\zhangdan.xls'

def open_xls(x):
    df_xls=pd.read_excel(x,encoding='utf-8') #导入发电费用
    return df_xls

def write_xls(x,sheet):
    writer = pd.ExcelWriter(jieguo) #输出到excel
    x.to_excel(writer, '%s_发单清单'%sheet)
    writer.save()
    return None

def main():  
    df_fadian=open_xls(fadian)
    df_zhanzhi=open_xls(zhanzhi)
    df_zhangdan=open_xls(zhangdan)

    col_name = list(df_fadian.columns)
    col_name.insert(col_name.index('站址来源（新建、存量）(不需填写）'),'当月发电次数')
    col_name.insert(col_name.index('铁塔审核发电开始时间'),'退服时长')
    col_name.insert(col_name.index('核减原因'),'剔除蓄电池保障3小时的时长')
    col_name.insert(col_name.index('发电日期'),'对应电信网管站址')
    col_name.insert(col_name.index('备注'),'发电是否及时')
    df_fadian=df_fadian.reindex(columns=col_name) 
    df_tmp = pd.read_excel(fadian,dtype=str,usecols=[6,7]) #从源表中用str读出7,8列因为站址编码、资源系统编码默认被识别为数字，造成数据丢失
    df_fadian['站址编码']=df_tmp['站址编码']      #将df_tmp['站址编码'] 赋值给'站址编码'列
    df_fadian['资源系统编码']=df_tmp['资源系统编码']    # 将df_tmp['资源系统编码'] 赋值给'资源系统编码'列
    df_tmp=pd.merge(df_tmp, df_zhanzhi, how='left', left_on='资源系统编码', right_on='铁塔公司物理站址编号' )
    df_fadian['对应电信网管站址']=df_tmp['对应电信应网管BTS/BBU名称'] 
    df_fadian['结算时长']=0
    df_fadian['结算次数']=0
    df_fadian['共享系数']=0
    df_fadian['油价']=0
    df_fadian['油费（不含税）']=0
    df_fadian['发电服务费（不含税）']=0
    df_fadian['总费用（不含税）']=0
    df_fadian['本月账单联合校验']=0
    tmp=df_fadian['共享系数']   #使用tmp变流量取出'共享系数'一列
    df_fadian.drop(labels=['共享系数'], axis=1,inplace = True)  #原表中删除'共享系数'一列
    df_fadian.insert(45,'共享系数',tmp)     #将‘共享系数’列插回到原表第46列
    df_fadian.fillna(0,inplace = True)
    data0=datetime.datetime.strptime('1970-01-01 00:00:00','%Y-%m-%d %H:%M:%S')    #生成停电时间为0时的时间data0
    cishu=df_fadian['资源系统编码'].value_counts()
    for i in range(0,len(df_fadian),1):
        df_fadian.loc[i,'当月发电次数']=cishu[df_fadian.loc[i,'资源系统编码']]
        df_fadian.loc[i,'结算时长']=df_fadian.loc[i,'剔除蓄电池保障3小时的时长']-max(df_fadian.loc[i,'核减时长'],df_fadian.loc[i,'退服时长'])
        df_fadian.loc[i,'共享系数']=len(df_fadian.loc[i,'CRM'].split('+'))
        if df_fadian.loc[i,'资源系统编码']=df_fadian.loc[i+1,'资源系统编码']:
            if df_fadian.loc[i,'发电日期']=df_fadian.loc[i+1,'发电日期']:
                df_fadian.loc[i,'结算次数']=0
            else df_fadian.loc[i,'结算次数']=1
        if  df_fadian.loc[i,'市电停电时间']==data0:  #当停电时间=0，即没有获取到停电时间
            fadian_time=df_fadian.loc[i,'铁塔审核发电结束时间']-df_fadian.loc[i,'铁塔审核发电开始时间']
            df_fadian.loc[i,'剔除蓄电池保障3小时的时长']=round(fadian_time.total_seconds()/60,0) 
        else:
            fadian_time=df_fadian.loc[i,'铁塔审核发电结束时间']-df_fadian.loc[i,'市电停电时间']-pd.Timedelta('0 days 3:0:00')
            df_fadian.loc[i,'剔除蓄电池保障3小时的时长']==round(fadian_time.total_seconds()/60)
    df_fadian['油费（不含税）']=df_fadian['结算时长'] /60*2.65 
    d2=df_fadian.iloc[1,12]
    sheet= d2.strftime('%Y-%m-%d %H:%M:%S')[:-12]   #从发电表取第14列第1行发电时间，格式化后，切片出月份：2017-11，做为输出excel的sheet名称
    write_xls(df_fadian,sheet)

if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    

