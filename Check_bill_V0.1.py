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
house=r'd:\2018年工作\2018年铁塔租费核对\new_house_bill.xls'
new_tower_bill=\
{'普通地面塔_H<30':15.8902,'普通地面塔_30≤H<35':18.3433,'普通地面塔_35≤H<40':21.6758,'普通地面塔_40≤H<45':25.4928,'普通地面塔_45≤H≤50':29.9715,
'景观塔_H<20':8.7872,'景观塔_20≤H<25':11.3222,'景观塔_25≤H<30':13.406,'景观塔_30≤H<35':18.2525,'景观塔_35≤H≤40':20.9292,
'简易塔_H≤20':3.9264,'普通楼面塔_-':4.0753,'楼面抱杆_-':1.2107,'无塔_H<30':0}
new_house_bill=pd.read_excel(house,dtype =str,encoding='utf-8').set_index()    #导入机房价格

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
    df_price=pd.DataFrame(columns=['账期月份','站址名称','站址编码','产品类型','机房类型','产品单元数',
    '计算铁塔价格','对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1',])
    df_price[['计算铁塔价格', '对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1']] \
    = df_price[['计算铁塔价格', '对应铁塔基准价格1','计算机房价格','对应机房基准价格1','计算配套价格','对应配套基准价格1','计算维护费','对应维护费1']]\
    .astype(float)      #将df_price中的价格列强制转换成float数据类型
    df_price['账期月份']=df_new['账期月份']
    df_price['站址名称']=df_new['站址名称']
    df_price['站址编码']=df_new['站址编码']
    df_price['产品类型']=df_new['产品类型']
    df_price['机房类型']=df_new['机房类型']
    df_price['产品单元数']=df_new['产品单元数1']
    df_price['对应铁塔基准价格1']=df_new['对应铁塔基准价格1']
    df_price['对应机房基准价格1']=df_new['对应机房基准价格1']
    df_price['对应配套基准价格1']=df_new['对应配套基准价格1']
    df_price['对应维护费1']=df_new['对应维护费1']
    for j in range(0,df_new['账期月份'].count(),1):
        df_price.loc[j,'计算铁塔价格']=(new_tower_bill[df_new.loc[j,'产品类型']+'_'+df_new.loc[j,'对应实际最高天线挂高（米）1']]*0.9/10)*1.02*1.15*10000/12
if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    
    
    