# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 11:12:29 2018

@author: Administrator
"""

import pandas as pd
import numpy as np
import os
import xlsxwriter
import matplotlib.pyplot as plt
from datetime import datetime


def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
    
    data_path = r'D:\MR报表\原始数据' + '\\'
    out_path = r'D:\MR报表\报表输出' + '\\'
    pic_path = r'D:\MR报表\pic' + '\\'
    
    MR_files = os.listdir(data_path)
    
    df_all = pd.DataFrame()
    
    for file in MR_files:
        df_tmp = pd.read_csv(data_path + file, engine = 'python', encoding = 'gbk')
        df_tmp = df_tmp[df_tmp['区域'] == '曲靖市']
        df_all = df_all.append(df_tmp)
    df_all['MR优良采样点'] =  df_all['|≥-105dBm采样点']+df_all['|≥-110dBm采样点']
    df_all['总采样点'] = df_all['|≥-105dBm采样点']+ df_all['|≥-110dBm采样点'] + df_all['|≥-115dBm采样点'] + df_all['|≥-120dBm采样点'] + df_all['|≥负无穷采样点']
    df_all_pivot = pd.pivot_table(df_all, index=['时间周期','区域','厂家','是否800M设备'], 
                                          values =['MR优良采样点','总采样点' ], 
                                          aggfunc = {'MR优良采样点':np.sum,'总采样点':np.sum})     
    df_city = pd.pivot_table(df_all_pivot, index=['时间周期','区域'], 
                                          values =['MR优良采样点','总采样点' ], 
                                          aggfunc = {'MR优良采样点':np.sum,'总采样点':np.sum})     
    
    df_all_pivot['MR优良率'] = df_all_pivot['MR优良采样点']/ df_all_pivot['总采样点']
    df_all_pivot['MR优良率'] = df_all_pivot['MR优良率']*100
    df_all_pivot = df_all_pivot.reset_index()
    df_all_pivot['时间周期'] = df_all_pivot['时间周期'].map(lambda x:x[5:])
    
    
    df_city['MR优良率'] = df_city['MR优良采样点']/ df_city['总采样点']
    df_city['MR优良率'] = df_city['MR优良率']*100
    df_city = df_city.reset_index()
    df_city['时间周期'] = df_city['时间周期'].map(lambda x:x[5:])
    
    # =============================================================================
    # 画全市MR优良率
    # =============================================================================
    y1 = df_city['MR优良率'].T.values
    x1 = df_city['时间周期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='MR优良率',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=10)
    plt.xlabel('日期')
    plt.ylabel('全市MR优良率')
    plt.title('全市MR优良率变化情况')
    plt.legend(loc='upper right')
    plt.savefig(pic_path + "全市MR优良率.png",format='png', dpi=400)  
    plt.close()
    
    # =============================================================================
    # 画中兴L1800优良率
    # =============================================================================
    df_zte = df_all_pivot[(df_all_pivot['厂家'] == '中兴')&(df_all_pivot['是否800M设备'] == '否')]
    y2 = df_zte['MR优良率'].T.values
    x2 = df_zte['时间周期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x2)), x2,fontsize=8)
    plt.plot(range(len(x2)),y2,label='MR优良率',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x2)),y2):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=10)
    plt.xlabel('日期')
    plt.ylabel('中兴1800_MR优良率')
    plt.title('中兴1800_MR优良率变化情况')
    plt.legend(loc='upper right')
    plt.savefig(pic_path + "中兴1800_MR优良率.png",format='png', dpi=400)  
    plt.close()
    
    # =============================================================================
    # 画中兴800M优良率
    # =============================================================================
    df_zte_800 = df_all_pivot[(df_all_pivot['厂家'] == '中兴')&(df_all_pivot['是否800M设备'] == '是')]
    y3 = df_zte_800['MR优良率'].T.values
    x3 = df_zte_800['时间周期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x3)), x3,fontsize=8)
    plt.plot(range(len(x3)),y3,label='MR优良率',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x3)),y3):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=10)
    plt.xlabel('日期')
    plt.ylabel('中兴800_MR优良率')
    plt.title('中兴800_MR优良率变化情况')
    plt.legend(loc='upper right')
    plt.savefig(pic_path + "中兴800_MR优良率.png",format='png', dpi=400)  
    plt.close()
    
    # =============================================================================
    # 画爱立信800M优良率
    # =============================================================================
    df_eric_800 = df_all_pivot[(df_all_pivot['厂家'] == '爱立信')&(df_all_pivot['是否800M设备'] == '是')]
    y4 = df_eric_800['MR优良率'].T.values
    x4 = df_eric_800['时间周期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x4)), x4,fontsize=8)
    plt.plot(range(len(x4)),y4,label='MR优良率',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x4)),y4):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=10)
    plt.xlabel('日期')
    plt.ylabel('爱立信800_MR优良率')
    plt.title('爱立信800_MR优良率变化情况')
    plt.legend(loc='upper right')
    plt.savefig(pic_path + "爱立信800_MR优良率.png",format='png', dpi=400)  
    plt.close()
    
    df_all['MR优良率'] = df_all['MR优良采样点']/ df_all['总采样点']
    df_all['MR优良率'] = df_all['MR优良率']*100
    df_all['权重'] = (df_all['总采样点']/sum(df_all['MR优良采样点']))*100
    df_all['权重'] = df_all['权重'].map(lambda x:round(x,5))
    
    df_top = df_all[df_all['MR优良率']<80]
    df_top_pivot = pd.pivot_table(df_top, index=['区域','NAME'], 
                                          values =['MR优良率','权重','厂家' ], 
                                          aggfunc = {'MR优良率':np.mean,'权重':np.mean,'厂家':len})     
    df_top_pivot.rename(columns={'厂家':'出现次数'},inplace =True)
    df_top_pivot = df_top_pivot.sort_values(by='权重',ascending = False)
    df_top_pivot = df_top_pivot.reset_index()
    
    with  pd.ExcelWriter(out_path + '本月MR指标.xlsx' ,engine='xlsxwriter')  as writer:  #输出到excel
        book = writer.book 
        sheet = book.add_worksheet('本月MR指标')
        sheet.insert_image('A2' , pic_path + "全市MR优良率.png")
        sheet.insert_image('A23', pic_path + "中兴1800_MR优良率.png")
        sheet.insert_image('A44', pic_path + "中兴800_MR优良率.png")
        sheet.insert_image('A65', pic_path + "爱立信800_MR优良率.png")
    
    with  pd.ExcelWriter(out_path  + 'TOP小区.xlsx')  as writer:  #输出到excel
        df_top_pivot.to_excel(writer, 'TOP小区')             

if __name__ == '__main__':
    main()



