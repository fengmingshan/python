# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 15:11:14 2018
fms learn python test github
@author: Administrator
"""
import pandas as pd   #导入pandas库
from pandas import DataFrame   #从pandas库导入数据框这种数据结构
import numpy as np   #导入numpy库    

old=r'd:\2018年工作\2018年铁塔租费核对\tower_201709.xls'
new=r'd:\2018年工作\2018年铁塔租费核对\tower_201710.xls'
house=r'd:\2018年工作\2018年铁塔租费核对\new_house_bill.xls'
new_tower_bill=\
{'普通地面塔_H<30':15.8902,'普通地面塔_30≤H<35':18.3433,'普通地面塔_35≤H<40':21.6758,'普通地面塔_40≤H<45':25.4928,'普通地面塔_45≤H<50':29.9715,
'景观塔_H<20':8.7872,'景观塔_H<20':11.3222,'景观塔_H<20':13.406,'景观塔_H<20':18.2525,'景观塔_H<20':20.9292,
'简易塔_H≤20':3.9264,'普通楼面塔':4.0753,'楼面抱杆':1.2107}
new_house_bill=pd.read_excel(house,dtype =str,encoding='utf-8')     #导入机房价格


def main():  
    df_old = pd.read_excel(old,dtype =str,encoding='utf-8')     #导入上月账单
    df_new = pd.read_excel(new,dtype =str,encoding='utf-8')     ##导入本月账单

    df_merge=pd.merge(df_old,df_new,how='right',on='产品业务确认单编号',suffixes=('上月','本月')) 
    # 对上月账单和本月账单进行右合并成df_merge，关键字是'产品业务确认单编号'，列标后面添加标识‘左表’和‘右表’
    df_merge.fillna('Null',inplace=True)    # 将df_merge中的空值填充为'Null'，因为空值就是没有值，不能进行筛选，比较等运算
    df_merge_left=pd.merge(df_old,df_new,how='right',on='产品业务确认单编号',suffixes=('上月','本月'))  
    # 对上月账单和本月账单进行左合并，关键字是'产品业务确认单编号'，列标后面添加标记‘左表和右表’
    df_merge_left.fillna('Null',inplace=True)  # 将 df_merge_left中的空值填充为'Null'，因为空值就是没有值，不能进行筛选，比较等运算
    
    """
    检查删除站址
    """  
    df_delete=df_merge[df_merge['账期月份本月']=='Null']   # 对左合并之后的表格筛选'账期月份本月'='Null'的行,
    df_delete=df_delete.set_index('产品业务确认单编号')    # 将'产品业务确认单编号'制定为index
    df_merge_left.drop(df_merge_left,axis=1,inplace=True)  #已经筛选出了删除的站点，左合并的表格df_merge_left就没有用处了，删除释放内存 
 
    """
    检查新增站址
    """
    df_add=df_merge[df_merge['账期月份上月']=='Null']     # 对右合并之后的表格筛选'账期月份上月'='Null'的行,
    df_add=df_add.set_index('产品业务确认单编号')    # 将'产品业务确认单编号'制定为index
    df_merge=df_merge[df_merge['账期月份上月']=='Null']  # 将本月新增的订单从df_merge中删除，以便后续的比对
    """
    逐列检查订单属性是否与上月相同
    """
    # 创建一个空表df_change，用于存放比对出来发生了变化的数据
    df_change=pd.DataFrame(columns=['是否发生变化','变化内容','铁塔站址名称','铁塔站址编码','上月值','本月值'])
    for i in range(10,147,1):        # 定义循环，i=10—146,从第10列开始比较。因为前9列不会发生变化
        df_change_tmp=df_merge.iloc[:,[6+146,7+146,i,i+146]]     # 取左表的第10列和右表的第十列构建一个新DataFrame：df_change_tmp
        df_change_tmp.columns = ['铁塔站址名称','铁塔站址编码','上月值','本月值']   # 修改新表的列标
        df_change_tmp.insert(0,'变化内容',df_merge.columns[i][:-2])   # 在df_change_tmp最前面插入一列 '变化内容'，该列的内容=左表第10列的列标切片去掉最右边2个字符'左表'
        df_change_tmp.insert(0,'是否发生变化',0)    # 在df_change_tmp最前面插入一列 '发生变化',内容=0
        df_change_tmp['是否发生变化']=~(df_change_tmp.iloc[:,4]==df_change_tmp.iloc[:,5])   # 对df_change_tmp列进行赋值=比较df_change_tmp第4列和第5列是否相等，然后取反
        df_change_tmp=df_change_tmp[df_change_tmp['是否发生变化']==True]    #对df_change_tmp筛选，'属性变化'列=True的内容
        df_change=pd.concat([df_change,df_change_tmp])     #筛选过的df_change_tmp合并在df_change后
    
    """
    逐行检查df_new的铁塔价格
    """
    # 创建一个空表df_price，用于存放比价格比对的数据
    df_price=pd.DataFrame(columns=['账期月份','铁塔站址名称','铁塔站址编码','产品类型','机房类型','产品单元数',
    '计算铁塔价格','对应铁塔基准价格1','计算机房价格','对机房基准价格1','计算配套价格','对配套基准价格1','计算维护费','对应维护费1',])
    df_price['账期月份']=df_new['账期月份']
    df_price['铁塔站址名称']=df_new['铁塔站址名称']
    df_price['铁塔站址编码']=df_new['铁塔站址编码']
    df_price['产品类型']=df_new['产品类型']
    df_price['机房类型']=df_new['机房类型']
    df_price['产品单元数']=df_new['产品单元数']
    for j in range(0,df_new[:,0].conut()+1,1):
        df_price.loc[j,'计算铁塔价格']=
    
    """
    将核查结果写入到excel中
    """
    writer = pd.ExcelWriter(r'd:\2018年工作\2018年铁塔租费核对\核查结果\核查结果.xls') #输出到excel
    df_change.to_excel(writer, '本月变化订单')
    df_delete.iloc[:,0:145].to_excel(writer, '本月退租订单')
    df_add.iloc[:,146:292].to_excel(writer, '本月新增订单')    
    writer.save()
   
if __name__=='__main__':        #python最终封装，python的固定格式
    main()
    