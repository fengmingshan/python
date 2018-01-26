# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 14:24:52 2018

@author: Administrator
"""
import pandas as pd   #导入pandas库
from pandas import DataFrame   #从pandas库导入数据框这种数据结构
import numpy as np   #导入numpy库    

old=r'd:\2018年工作\2018年铁塔租费核对\tower_201709.xls'
new=r'd:\2018年工作\2018年铁塔租费核对\tower_201710.xls'
tieta=r'd:\2018年工作\2018年铁塔租费核对\tieta_bill.xls'
jifang=r'd:\2018年工作\2018年铁塔租费核对\jifang_bill.xls'
peitao=r'd:\2018年工作\2018年铁塔租费核对\peitao_bill.xls'
weihu=r'd:\2018年工作\2018年铁塔租费核对\weihu_bill.xls'
zhejiu={'普通地面塔':20,'景观塔':6,'简易塔':6,'普通楼面塔':6,'楼面抱杆':6,'无塔':6}	#定义折旧年限的字典


tieta_bill=pd.read_excel(tieta,dtype =str,encoding='utf-8') #导入铁塔价格
tieta_bill=tieta_bill.set_index('产品类型')	#将jifang_bill的index设置为'产品类型'，主要是为了后面按行列索引进行切片操作
tieta_bill.iloc[:,0:]=tieta_bill.iloc[:,0:].astype(float)   #将tieta_bill的所有列强制转化成float数据类型。

jifang_bill=pd.read_excel(jifang,dtype =str,encoding='utf-8') #导入机房价格
jifang_bill=jifang_bill.set_index('产品类型')	  #将jifang_bill的index设置为'产品类型'，主要是为了后面按行列索引进行切片操作
jifang_bill.iloc[:,0:]=jifang_bill.iloc[:,0:].astype(float)   #将jifang_bill的所有列强制转化成float数据类型。

peitao_bill=pd.read_excel(peitao,dtype =str,encoding='utf-8') #导入配套价格
peitao_bill=peitao_bill.set_index('产品类型')	  #将peitao_bill的index设置为'产品类型'，主要是为了后面按行列索引进行切片操作
peitao_bill.iloc[:,0:]=peitao_bill.iloc[:,0:].astype(float)     #将peitao_bill的所有列强制转化成float数据类型。

weihu_bill=pd.read_excel(weihu,dtype =str,encoding='utf-8') #导入维护价格
weihu_bill=weihu_bill.set_index('运营商区县')	  #将peitao_bill的index设置为'产品类型'，主要是为了后面按行列索引进行切片操作
weihu_bill.iloc[:,0:]=weihu_bill.iloc[:,0:].astype(float)     #将peitao_bill的所有列强制转化成float数据类型。


def main():  

    """
    逐行检查df_new的铁塔价格
    """
    df_new = pd.read_excel(new,dtype =str,encoding='utf-8')     ##导入本月账单
    df_new.fillna('Null',inplace=True)   #将表格中的空值填充为NULL
    df_new=df_new[df_new['业务属性'].isin(['塔'])]  #剔除非标顶单和业务属性为空的订单
    print(df_new['账期月份'].count()+1)
    df_new=df_new.set_index(np.arange(0,df_new['账期月份'].count(),1))

    # 创建一个空表df_price，用于存放比价格比对的数据
    df_price=pd.DataFrame(columns=['账期月份','运营商区县','站址名称','站址编码','产品类型','机房类型','产品单元数',
    '计算铁塔价格','对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1','订单属性','产权属性','原产权方',])
    df_price['账期月份']=df_new['账期月份']
    df_price['运营商区县']=df_new['运营商区县']
    df_price['站址名称']=df_new['站址名称']
    df_price['站址编码']=df_new['站址编码']
    df_price['产品类型']=df_new['产品类型']
    df_price['机房类型']=df_new['机房类型']
    df_price['产品单元数']=df_new['产品单元数1']
    df_price['对应铁塔基准价格1']=df_new['对应铁塔基准价格1']
    df_price['对应机房基准价格1']=df_new['对应机房基准价格1']
    df_price['对应配套基准价格1']=df_new['对应配套基准价格1']
    df_price['对应维护费1']=df_new['对应维护费1']
    df_price['订单属性']=df_new['订单属性']
    df_price['产权属性']=df_new['产权属性']
    df_price['原产权方']=df_new['原产权方']
    
   
    
    #下面要通过数学计算算出各种产品价格，所以先要对数据列进行一些处理，因为我们导入表格的时候dtype =str,所有的列都是str型，不能做数学运算
    df_price[['产品单元数','计算铁塔价格', '对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1']] \
    = df_price[['产品单元数','计算铁塔价格', '对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1']]\
    .astype(float)      #将df_price中有产品价格列强制转换成float数据类型,如果不转换的话，
    for j in range(0,df_price['账期月份'].count(),1):
        df_price.loc[j,'计算维护费']=df_price.loc[j,'产品单元数']*\
        weihu_bill.at[df_price.loc[j,'运营商区县'],df_price.loc[j,'机房类型']]*1.15/12

        if df_new.loc[j,'产权属性']=='注入':
            df_price.loc[j,'计算铁塔价格']=df_price.loc[j,'产品单元数']*\
            (tieta_bill.at[df_new.loc[j,'产品类型'],df_new.loc[j,'对应实际最高天线挂高（米）1']]*0.7/10)*1.02*1.15*10000/12
            df_price.loc[j,'计算机房价格']=df_price.loc[j,'产品单元数']*\
            (jifang_bill.at[df_price.loc[j,'产品类型'],df_price.loc[j,'机房类型']]*0.7/zhejiu[df_price.loc[j,'产品类型']])*1.02*1.15*10000/12
            df_price.loc[j,'计算配套价格']=df_price.loc[j,'产品单元数']*\
            (peitao_bill.at[df_price.loc[j,'产品类型'],df_price.loc[j,'机房类型']]*0.7/6)*1.02*1.15*10000/12
        elif df_new.loc[j,'产权属性']=='自建':
            df_price.loc[j,'计算铁塔价格']=df_price.loc[j,'产品单元数']*\
            (tieta_bill.at[df_new.loc[j,'产品类型'],df_new.loc[j,'对应实际最高天线挂高（米）1']]*0.9/10)*1.02*1.15*10000/12
            df_price.loc[j,'计算机房价格']=df_price.loc[j,'产品单元数']*\
            (jifang_bill.at[df_price.loc[j,'产品类型'],df_price.loc[j,'机房类型']]*0.9/zhejiu[df_price.loc[j,'产品类型']])*1.02*1.15*10000/12
            df_price.loc[j,'计算配套价格']=df_price.loc[j,'产品单元数']*\
            (peitao_bill.at[df_price.loc[j,'产品类型'],df_price.loc[j,'机房类型']]*0.9/6)*1.02*1.15*10000/12
    
    writer = pd.ExcelWriter(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls') #输出到excel
    df_price.to_excel(writer, '本月订单价格变化')
    writer.save()
if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    
    
    