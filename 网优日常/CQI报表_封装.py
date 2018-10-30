# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 11:17:24 2018

@author: Administrator
"""

import pandas as pd 
import os
import numpy as np
from datetime import datetime 
import matplotlib.pyplot as plt

def main():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

    current_date = str(datetime.now()).split('.')[0].split(' ')[0]
    
    data_path = r'D:\CQI报表\原始数据' + '\\'
    out_path = r'D:\CQI报表' + '\\'
    pic_path = r'D:\CQI报表\pic' + '\\'
    PhyChannel1 = 'PhyChannel_OMMB1.xlsx' 
    PhyChannel2 = 'PhyChannel_OMMB2.xlsx'
    
    cell_name = 'cell_name.xlsx'
    
    df_OMMB1 = pd.read_excel(out_path + PhyChannel1 ,encoding='utf-8') 
    df_OMMB2 = pd.read_excel(out_path + PhyChannel2 ,encoding='utf-8') 
    df_OMMB1 = df_OMMB1.drop([0,1,2])
    df_OMMB2 = df_OMMB2.drop([0,1,2])
    
    df_OMMB1.rename(columns={'RESULT':'OMMB'},inplace =True)
    df_OMMB2.rename(columns={'RESULT':'OMMB'},inplace =True)
    df_OMMB1['OMMB'] = 'OMMB1'
    df_OMMB2['OMMB'] = 'OMMB2'
    df_PhyChannel = df_OMMB1.append(df_OMMB2)
    df_PhyChannel = df_PhyChannel[['OMMB','MOI','SubNetwork','MEID','description','cqiRptPeriod']]
    df_PhyChannel['MOI'] = df_PhyChannel['MOI'].map(lambda x:x.replace('ConfigSet=0,',''))
    df_PhyChannel['description'] = df_PhyChannel['description'].map(lambda x:x.split('=')[1])
    df_PhyChannel['description'] = df_PhyChannel['MEID'] + '_' + df_PhyChannel['description']
    df_PhyChannel.rename(columns={'description':'小区编码'},inplace =True)
    
    files = os.listdir(data_path)
    df_yunnan = pd.DataFrame()
    for file in files:
        df_tmp = pd.read_csv(data_path + file ,engine= 'python',encoding='gbk')
        df_yunnan = df_yunnan.append(df_tmp)
    
    df_yunnan_pivot = pd.pivot_table(df_yunnan, index=['区域'], 
                                      values =['CQI上报总次数' ,'CQI大于等于7次数'], 
                                      aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
    df_yunnan_pivot['CQI优良比'] = df_yunnan_pivot['CQI大于等于7次数'] / df_yunnan_pivot['CQI上报总次数'] 
    df_yunnan_pivot = df_yunnan_pivot.sort_values(by='CQI优良比',ascending = False)
    df_yunnan_pivot = df_yunnan_pivot.reset_index()          
    
    
    df_qujing = df_yunnan[(df_yunnan['区域'] == '曲靖市')]
    df_qujing_pivot = pd.pivot_table(df_qujing, index=['日期'], 
                                              values =['CQI上报总次数' ,'CQI大于等于7次数'], 
                                              aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
    df_qujing_pivot = df_qujing_pivot.reset_index()          
    df_qujing_pivot.rename(columns={'CQI上报总次数':'CQI全天总数','CQI大于等于7次数':'CQI大于等于7全天总数'},inplace =True)
    df_qujing_pivot['CQI优良比_全市'] =  df_qujing_pivot['CQI大于等于7全天总数']/df_qujing_pivot['CQI全天总数']
    
    
    df_qujing_zte  = df_yunnan[(df_yunnan['区域'] == '曲靖市')&(df_yunnan['厂家'] == '中兴')]
    df_zte_day = pd.pivot_table(df_qujing_zte, index=['日期','区域'], 
                                                   values =['CQI上报总次数','CQI大于等于7次数' ], 
                                                   aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
    df_zte_day = df_zte_day.reset_index()    
    df_zte_day['CQI优良比'] =  df_zte_day['CQI大于等于7次数']/df_zte_day['CQI上报总次数']
    
    df_qujing_eric  = df_yunnan[(df_yunnan['区域'] == '曲靖市')&(df_yunnan['厂家'] == '爱立信')]
    df_eric_day = pd.pivot_table(df_qujing_eric, index=['日期','区域'], 
                                                   values =['CQI上报总次数','CQI大于等于7次数' ], 
                                                   aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})     
    df_eric_day = df_eric_day.reset_index()    
    df_eric_day['CQI优良比'] =  df_eric_day['CQI大于等于7次数']/df_eric_day['CQI上报总次数']
    
    print('---------汇总原始数据完成！---------')
    
    # =============================================================================
    # 质优小区
    # =============================================================================
    df_zte_good = df_qujing_zte[df_qujing_zte['CQI大于等于7比例']>90]   
    df_zte_good.rename(columns={'厂家':'小区编码','CQI大于等于7比例':'CQI优良比'},inplace =True)
    df_zte_good['小区编码'] = df_zte_good['小区名'].map(lambda x:str(x).split('R')[0][:-1])
    df_zte_good = pd.merge(df_zte_good,df_PhyChannel,how='left',on='小区编码')
    df_zte_good = pd.merge(df_zte_good,df_qujing_pivot,how='left',on='日期')
    df_zte_good = df_zte_good[['区域','日期','小区名','小区编码','是否800M设备','CQI上报总次数',\
                               'CQI大于等于7次数','CQI优良比','OMMB','MOI','SubNetwork','MEID',\
                               'cqiRptPeriod','CQI全天总数','CQI大于等于7全天总数']]
    df_zte_good['权重'] = df_zte_good['CQI上报总次数']/df_zte_good['CQI全天总数']
    date_now = df_zte_good.loc[len(df_zte_good)-1,'日期']
    df_zte_good = df_zte_good[df_zte_good['日期'] == date_now]
    df_zte_good = df_zte_good.sort_values(by='权重',ascending = False) # 按权重降序排列  
    
    # =============================================================================
    # 质差小区
    # =============================================================================
    df_zte_worse = df_qujing_zte[df_qujing_zte['CQI大于等于7比例']<90]  
    df_zte_worse.rename(columns={'厂家':'小区编码','CQI大于等于7比例':'CQI优良比'},inplace =True)
    df_zte_worse['小区编码'] = df_zte_worse['小区名'].map(lambda x:str(x).split('R')[0][:-1])
    df_zte_worse = pd.merge(df_zte_worse,df_PhyChannel,how='left',on='小区编码')
    df_zte_worse = pd.merge(df_zte_worse,df_qujing_pivot,how='left',on='日期')
    df_zte_worse = df_zte_worse[['区域','日期','小区名','小区编码','是否800M设备','CQI上报总次数',\
                               'CQI大于等于7次数','CQI优良比','OMMB','MOI','SubNetwork','MEID',\
                               'cqiRptPeriod','CQI全天总数','CQI大于等于7全天总数']]
    df_zte_worse['权重'] = df_zte_worse['CQI上报总次数']/df_zte_worse['CQI全天总数']
    date_now = df_zte_worse.loc[len(df_zte_worse)-1,'日期']
    df_zte_worse = df_zte_worse[df_zte_worse['日期'] == date_now]
    df_zte_worse = df_zte_worse.sort_values(by='权重',ascending = False) # 按权重降序排列  
    
    # =============================================================================
    # 画全省CQI优良率
    # =============================================================================
    y = df_yunnan_pivot['CQI优良比'].map(lambda x:x*100).T.values
    city_list = df_yunnan_pivot['区域'].T.values
    plt.figure(figsize=(12, 4))
    x_city = range(0,len(city_list)) 
    plt.bar(x_city,y,color='b',width = 0.3,alpha=0.6,label='全省CQI优良比')
    for x,y in zip(x_city,y):
        plt.text(x, y*1.001,'%.2f%%' % y, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('全省CQI优良比')
    plt.xticks(range(0,len(city_list)),city_list)
    plt.ylabel('城市')
    plt.legend(loc='center right')
    plt.title('全省CQI优良比')
    plt.savefig(pic_path + "全省CQI优良比.png",format='png', dpi=200) 
    plt.close()
    
    # =============================================================================
    # 画全市CQI优良率
    # =============================================================================
    y1 = df_qujing_pivot['CQI优良比_全市'].map(lambda x:x*100).T.values
    x1 = df_qujing_pivot['日期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
    plt.xlabel('日期')
    plt.ylabel('全市CQI优良比')
    plt.title('全市CQI优良比变化情况')
    plt.legend(loc='center right')
    plt.savefig(pic_path + "全市CQI优良比.png",format='png', dpi=400)  
    plt.close()
    
    # =============================================================================
    # 画中兴CQI优良率
    # =============================================================================
    y1 = df_zte_day['CQI优良比'].map(lambda x:x*100).T.values
    x1 = df_zte_day['日期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
    plt.xlabel('日期')
    plt.ylabel('中兴CQI优良比')
    plt.title('中兴CQI优良比变化情况')
    plt.legend(loc='center right')
    plt.savefig(pic_path + "中兴CQI优良比.png",format='png', dpi=400)  
    plt.close()
    
    # =============================================================================
    # 画爱立信CQI优良率
    # =============================================================================
    y1 = df_eric_day['CQI优良比'].map(lambda x:x*100).T.values
    x1 = df_eric_day['日期'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='CQI优良比',linewidth=3,color='r',marker='o',markerfacecolor='blue',markersize=6) 
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001,  '%.2f%%' % b, ha='center', va= 'bottom',fontsize=9)
    plt.xlabel('日期')
    plt.ylabel('爱立信CQI优良比')
    plt.title('爱立信CQI优良比变化情况')
    plt.legend(loc='center right')
    plt.savefig(pic_path + "爱立信CQI优良比.png",format='png', dpi=400)  
    plt.close()
    
    print('---------图表绘制完成！---------')

    # =============================================================================
    # 生成ommb1修改指令
    # =============================================================================
    df_good_ommb1 = df_zte_good[(df_zte_good['cqiRptPeriod'] != '1;2;3')&(df_zte_good['OMMB'] == 'OMMB1')]
    df_worse_ommb1 = df_zte_worse[(df_zte_worse['cqiRptPeriod'] != '3;4;5')&(df_zte_worse['OMMB'] == 'OMMB1')]
    df_good_ommb1 = df_good_ommb1.reset_index()
    df_worse_ommb1 = df_worse_ommb1.reset_index()
    
    
    with open(out_path + 'apply_right_OMMB1.txt','a') as f:
        for i in range(0,len(df_good_ommb1),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_good_ommb1.loc[i,'SubNetwork'],
                    df_good_ommb1.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    with open(out_path + 'apply_right_OMMB1.txt','a') as f:
        for i in range(0,len(df_worse_ommb1),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_worse_ommb1.loc[i,'SubNetwork'],
                    df_worse_ommb1.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    with open(out_path + 'OMMB1_command.txt','a') as f:
        for i in range(0,len(df_good_ommb1),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;2;3\"",EXTENDS="";'\
            .format(df_good_ommb1.loc[i,'MOI'])
            f.write(line+'\n') 
    
    with open(out_path + 'OMMB1_command.txt','a') as f:
        for i in range(0,len(df_worse_ommb1),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"3;4;5\"",EXTENDS="";'\
            .format(df_worse_ommb1.loc[i,'MOI'])
            f.write(line+'\n') 
    
    # =============================================================================
    # 生成ommb2修改指令
    # =============================================================================
    
    df_good_ommb2 = df_zte_good[(df_zte_good['cqiRptPeriod'] != '1;2;3')&(df_zte_good['OMMB'] == 'OMMB2')]
    df_worse_ommb2 = df_zte_worse[(df_zte_worse['cqiRptPeriod'] != '3;4;5')&(df_zte_worse['OMMB'] == 'OMMB2')]
    df_good_ommb2 = df_good_ommb2.reset_index()
    df_worse_ommb2 = df_worse_ommb2.reset_index()
    
    with open(out_path + 'apply_right_OMMB2.txt','a') as f:
        for i in range(0,len(df_good_ommb2),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_good_ommb2.loc[i,'SubNetwork'],
                    df_good_ommb2.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    with open(out_path + 'apply_right_OMMB2.txt','a') as f:
        for i in range(0,len(df_worse_ommb2),1):
            line = r'APPLY MUTEXRIGHT:SUBNET="{0}",NE="{1}";'\
            .format(df_worse_ommb2.loc[i,'SubNetwork'],
                    df_worse_ommb2.loc[i,'MEID'],
    )
            f.write(line+'\n')         
    
    with open(out_path + 'OMMB2_command.txt','a') as f:
        for i in range(0,len(df_good_ommb2),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"1;2;3\"",EXTENDS="";'\
            .format(df_good_ommb2.loc[i,'MOI'])
            f.write(line+'\n') 
    
    with open(out_path + 'OMMB2_command.txt','a') as f:
        for i in range(0,len(df_worse_ommb2),1):
            line = r'UPDATE:MOC="PhyChannel",MOI="{0}",ATTRIBUTES="cqiRptPeriod=\"3;4;5\"",EXTENDS="";'\
            .format(df_worse_ommb2.loc[i,'MOI'])
            f.write(line+'\n') 
    
    with  pd.ExcelWriter(out_path + '曲靖CQI优良率' + current_date + '.xlsx')  as writer:  #输出到excel
        book = writer.book 
        sheet = book.add_worksheet('本月MR指标')
        sheet.insert_image('A2' , pic_path + "全省CQI优良比.png")
        sheet.insert_image('A23', pic_path + "全市CQI优良比.png")
        sheet.insert_image('A44', pic_path + "中兴CQI优良比.png")
        sheet.insert_image('A65', pic_path + "爱立信CQI优良比.png")
        df_zte_good.to_excel(writer,'质优小区') 
        df_zte_worse.to_excel(writer,'质差小区') 

    print('---------修改指令输出完成！---------')


if __name__ == '__main__':
    main()
