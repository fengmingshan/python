# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:24:12 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号

#设置工作和参数

current_date = str(datetime.now()).split('.')[0].split(' ')[0]
data_path = r'D:\_VoLTE网络健康检查（日）' + '\\'
expect_success_rate = 99
expect_drop_rate = 0.3
min_call_num = 3
min_drop_num = 3

# =============================================================================
# 采集原始数据文件及创建所需工作目录
# =============================================================================
all_files = os.listdir(data_path)
files = [x for x in all_files if '.csv' in x ]

if '报表输出' not in all_files:
    os.makedirs(data_path + '报表输出' + '\\' )
report_path = data_path + '报表输出' + '\\'

if 'PIC' not in all_files:
    os.makedirs(data_path + 'PIC' + '\\' )
pic_path = data_path + 'PIC' + '\\'

df_cell = pd.DataFrame()
df_subnet = pd.DataFrame()
df_city = pd.DataFrame()

for file in files:
   if '历史性能' in file:
       df_tmp = pd.read_csv(data_path + file,engine = 'python',skiprows = 5 )
       columns = list(df_tmp.columns)
       if '小区名称' in columns:
           df_cell = df_cell.append(df_tmp)
       elif '子网名称' in columns and '小区名称' not in columns:
           df_subnet = df_subnet.append(df_tmp)
       else :
           df_city = df_city.append(df_tmp)
   else:
       df_tmp = pd.read_csv(data_path + file,engine = 'python')
       columns = list(df_tmp.columns)
       if '小区名称' in columns:
           df_cell = df_cell.append(df_tmp)
       elif '子网名称' in columns and '小区名称' not in columns:
           df_subnet = df_subnet.append(df_tmp)
       else :
           df_city = df_city.append(df_tmp)

KPI_date = df_city.loc[0,'开始时间'].split(' ')[0]

# =============================================================================
# 全市昨日VOLTE指标分析
# =============================================================================
def draw_KPI(df,text):
    '''画VOLTE关键指标图'''
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    # 画VOLTE户数
    y1 = df['[LTE]下行QCI1最大激活用户数'].T.values
    y2 = df['[LTE]下行QCI2最大激活用户数'].T.values
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4)
    plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4)
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE用户数')
    plt.title(text + '_VOLTE用户数')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE用户数.png",format='png', dpi=400)
    plt.close

    # 画VOLTE呼叫次数
    y1 = df['[LTE]E-RAB建立请求数目(QCI=1)'].T.values
    y2 = df['[LTE]E-RAB建立请求数目(QCI=2)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音用户数',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4)
    plt.plot(range(len(x1)),y2,label='VOLTE视频用户数',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4)
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, b, ha='center', va= 'bottom',fontsize=12)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE呼叫数')
    plt.title(text + '_VOLTE呼叫数')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text +  "VOLTE呼叫次数.png",format='png', dpi=400)
    plt.close


    # 画VOLTE掉话率
    y1 = df['[FDD]E-RAB掉话率(QCI=1)'].T.values
    y2 = df['[FDD]E-RAB掉话率(QCI=2)'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音掉话率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=4)
    plt.plot(range(len(x1)),y2,label='VOLTE视频掉话率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=4)
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.001, '%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.001, '%.2f%%'% b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE掉话率')
    plt.title(text + '_VOLTE掉话率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE掉话率.png",format='png', dpi=400)
    plt.close

    # 画VOLTE语音接通率
    y1 = df['[LTE]小区E-RAB建立成功率，QCI=1'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y1,label='VOLTE语音接通率',linewidth=2,color='r',marker='o',markerfacecolor='blue',markersize=5)
    for a,b in zip(range(len(x1)),y1):
        plt.text(a,b*1.0001,'%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE语音接通率')
    plt.title(text + '_VOLTE语音接通率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE语音接通率.png",format='png', dpi=400)
    plt.close

    # 画VOLTE视频接通率
    y2 = df['[LTE]小区E-RAB建立成功率，QCI=2'].T.values
    df['hour'] = df['开始时间'].map(lambda x:x[11:13])
    x1 = df['hour'].T.values
    plt.figure(figsize=(12, 4))
    plt.xticks(range(len(x1)), x1,fontsize=8)
    plt.plot(range(len(x1)),y2,label='VOLTE视频接通率',linewidth=2,color='g',marker='o',markerfacecolor='cyan',markersize=5)
    for a,b in zip(range(len(x1)),y2):
        plt.text(a,b*1.0001, '%.2f%%' % b, ha='center', va= 'bottom',fontsize=8)
    plt.xlabel('小时')
    plt.ylabel(text + '_VOLTE视频接通率')
    plt.title(text + '_VOLTE视频接通率')
    plt.legend(loc='center right')
    plt.savefig(pic_path + text + "VOLTE视频接通率.png",format='png', dpi=400)
    plt.close


df_city['[FDD]E-RAB掉话率(QCI=1)'] = df_city['[FDD]E-RAB掉话率(QCI=1)'].str.strip("%").astype(float)
df_city['[FDD]E-RAB掉话率(QCI=2)'] = df_city['[FDD]E-RAB掉话率(QCI=2)'].str.strip("%").astype(float)
df_city['[LTE]小区E-RAB建立成功率，QCI=1'] = df_city['[LTE]小区E-RAB建立成功率，QCI=1'].str.strip("%").astype(float)
df_city['[LTE]小区E-RAB建立成功率，QCI=2'] = df_city['[LTE]小区E-RAB建立成功率，QCI=2'].str.strip("%").astype(float)

draw_KPI(df_city,'全市')

# =============================================================================
# 各区县指标绘制
# =============================================================================
df_subnet['子网名称'] = df_subnet['子网名称'].map(lambda x:x.replace('曲靖','').split('(')[0].split(' ')[0])
df_subnet['[FDD]E-RAB掉话率(QCI=1)'] = df_subnet['[FDD]E-RAB掉话率(QCI=1)'].str.strip("%").astype(float)
df_subnet['[FDD]E-RAB掉话率(QCI=2)'] = df_subnet['[FDD]E-RAB掉话率(QCI=2)'].str.strip("%").astype(float)
df_subnet['[LTE]小区E-RAB建立成功率，QCI=1'] = df_subnet['[LTE]小区E-RAB建立成功率，QCI=1'].str.strip("%").astype(float)
df_subnet['[LTE]小区E-RAB建立成功率，QCI=2'] = df_subnet['[LTE]小区E-RAB建立成功率，QCI=2'].str.strip("%").astype(float)

subnet_name = sorted(list(set(df_subnet['子网名称'])))
TOP_country_name = []
for name in subnet_name:
    df_country =  df_subnet[df_subnet['子网名称'] == name]
    if df_country['[LTE]小区E-RAB建立成功率，QCI=1'].max() < expect_success_rate  or \
    df_country['[FDD]E-RAB掉话率(QCI=1)'].max() > expect_drop_rate :
         TOP_country_name.append(name)
         draw_KPI(df_country,name)
# =============================================================================
# TOP小区分析
# =============================================================================
df_cell['hour'] = df_cell['开始时间'].map(lambda x:x[11:13])
df_cell['[LTE]E-RAB建立请求数目(QCI=1)'] = df_cell['[LTE]E-RAB建立请求数目(QCI=1)'].astype(int)
df_cell['[LTE]小区E-RAB建立成功率，QCI=1'] = df_cell['[LTE]小区E-RAB建立成功率，QCI=1'].str.strip("%").astype(float)
df_cell['[FDD]E-RAB掉话率(QCI=1)'] = df_cell['[FDD]E-RAB掉话率(QCI=1)'].str.strip("%").astype(float)

# =============================================================================
# 呼叫成功率TOP分析
# =============================================================================
df_connect_top = df_cell[(df_cell['[LTE]E-RAB建立请求数目(QCI=1)'] > min_call_num ) & (df_cell['[LTE]小区E-RAB建立成功率，QCI=1'] <= expect_success_rate)]
df_connect_top['原因分析'] = ''
df_connect_top = df_connect_top[['开始时间', '结束时间','子网名称','网元','小区','小区名称','原因分析',
                                 '[LTE]小区E-RAB建立成功率，QCI=1',
                                 '[LTE]E-RAB建立请求数目(QCI=1)',
                                 '[LTE]E-RAB建立成功数目(QCI=1)',
                                 'QCI1 初始的E-RAB建立成功次数',
                                 'QCI1 增加的E-RAB建立成功次数',
                                 'QCI1 初始的E-RAB建立失败次数，空口失败',
                                 'QCI1 初始的E-RAB建立失败次数，eNB接纳失败',
                                 'QCI1 初始的E-RAB建立失败次数，RRC重建立原因',
                                 'QCI1 初始的E-RAB建立失败次数，传输层原因',
                                 'QCI1 初始的E-RAB建立失败次数，消息参数错误',
                                 'QCI1 初始的E-RAB建立失败次数，安全激活失败',
                                 'QCI1 初始的E-RAB建立失败次数，其他原因',
                                 'QCI1 增加的E-RAB建立失败次数，空口失败',
                                 'QCI1 增加的E-RAB建立失败次数，切换引起',
                                 'QCI1 增加的E-RAB建立失败次数，eNB接纳失败',
                                 'QCI1 增加的E-RAB建立失败次数，RRC重建立原因',
                                 'QCI1 增加的E-RAB建立失败次数，传输层原因',
                                 'QCI1 增加的E-RAB建立失败次数，消息参数错误',
                                 'QCI1 增加的E-RAB建立失败次数，其他原因'
]]
df_connect_top['失败总次数'] = df_connect_top['[LTE]E-RAB建立请求数目(QCI=1)'] -\
                              df_connect_top['[LTE]E-RAB建立成功数目(QCI=1)']
df_connect_top['空口问题占比'] = (df_connect_top['QCI1 初始的E-RAB建立失败次数，空口失败'] +
                                 df_connect_top['QCI1 增加的E-RAB建立失败次数，空口失败'] +
                                 df_connect_top['QCI1 初始的E-RAB建立失败次数，RRC重建立原因'] +
                                 df_connect_top['QCI1 增加的E-RAB建立失败次数，RRC重建立原因'])\
                                /df_connect_top['失败总次数']
df_connect_top['拥塞占比'] = (df_connect_top['QCI1 初始的E-RAB建立失败次数，eNB接纳失败'] +
                              df_connect_top['QCI1 增加的E-RAB建立失败次数，eNB接纳失败'])\
                              /df_connect_top['失败总次数']
df_connect_top['传输故障占比'] = (df_connect_top['QCI1 初始的E-RAB建立失败次数，传输层原因'] +
                                  df_connect_top['QCI1 增加的E-RAB建立失败次数，传输层原因'])\
                                  /df_connect_top['失败总次数']
df_connect_top['参数或软件故障占比'] = (df_connect_top['QCI1 初始的E-RAB建立失败次数，消息参数错误'] +
                                  df_connect_top['QCI1 增加的E-RAB建立失败次数，消息参数错误']) \
                                  /df_connect_top['失败总次数']
df_connect_top['安全激活失败'] = df_connect_top['QCI1 初始的E-RAB建立失败次数，安全激活失败'] / df_connect_top['失败总次数']
df_connect_top['切换问题占比'] = df_connect_top['QCI1 增加的E-RAB建立失败次数，切换引起'] / df_connect_top['失败总次数']
df_connect_top['其他原因占比'] = (df_connect_top['QCI1 初始的E-RAB建立失败次数，其他原因'] +
                                  df_connect_top['QCI1 增加的E-RAB建立失败次数，其他原因']) \
                                   /df_connect_top['失败总次数']
df_connect_top = df_connect_top.sort_values(by=['[LTE]E-RAB建立请求数目(QCI=1)','[LTE]小区E-RAB建立成功率，QCI=1'],ascending = [False,True]) # 按时间顺序升序排列
df_connect_top.fillna(0,inplace = True)

def findmax(df):  # 定义找最大值的函数
    max_one = df.idxmax() # 得到最大值的index名
    maxindex = pd.Series(max_one) # 将每一行的最大值的index重组成一个Series
    return maxindex  # 返回这个Series

df_tmp  = df_connect_top.iloc[:,28:37] # 只取我们需要的列构建一个零时的表

df_tmp['问题主要原因'] = df_tmp.apply(lambda x:findmax(x),axis=1) # 将表按行输入找最大值的函数，得到最大值所在的列的index

df_connect_top['原因分析'] = df_tmp['问题主要原因']
fault_cause = {'空口问题占比':'无线环境差',
               '拥塞占比':'基站资源拥塞',
               '传输故障占比':'传输故障',
               '参数或软件故障占比':'参数或软件版本故障',
               '安全激活失败':'手机软件问题',
               '切换问题占比':'切换问题',
               '其他原因占比':'其他原因(不明)',
}

df_connect_top['原因分析'] = df_connect_top['原因分析'].map(fault_cause)

# =============================================================================
# 掉话率TOP小区分析
# =============================================================================
df_drop_top = df_cell[(df_cell['[FDD]E-RAB掉话率(QCI=1)'] > expect_drop_rate ) & (df_cell['[LTE]E-RAB建立成功数目(QCI=1)'] > min_drop_num)]
df_drop_top['原因分析'] = ''
df_drop_top = df_drop_top[['开始时间', '结束时间','子网名称','网元','小区','小区名称','原因分析',
                           '[FDD]E-RAB掉话率(QCI=1)',
                           '[LTE]E-RAB建立成功数目(QCI=1)',
                           'QCI1 E-RAB释放次数，由于ENB小区拥塞导致的释放',
                           'QCI1 E-RAB释放次数，由于ENB过载控制导致的释放',
                           'QCI1 E-RAB释放次数，由于ENB的无线链路失败',
                           'QCI1 E-RAB释放次数，由于ENB重建立失败',
                           'QCI1 E-RAB释放次数，由于小区关断或复位',
                           'QCI1 E-RAB释放次数，跨站重建立失败导致的释放',
                           'QCI1 E-RAB释放次数，ENB由于S1链路故障发起释放',
                           'QCI1 E-RAB释放次数，由于ENB其他异常原因',
]]
df_drop_top['掉话总次数'] = df_drop_top['QCI1 E-RAB释放次数，由于ENB小区拥塞导致的释放'] +\
                              df_drop_top['QCI1 E-RAB释放次数，由于ENB过载控制导致的释放'] +\
                              df_drop_top['QCI1 E-RAB释放次数，由于ENB的无线链路失败'] +\
                              df_drop_top['QCI1 E-RAB释放次数，由于ENB重建立失败'] +\
                              df_drop_top['QCI1 E-RAB释放次数，由于小区关断或复位'] +\
                              df_drop_top['QCI1 E-RAB释放次数，跨站重建立失败导致的释放'] +\
                              df_drop_top['QCI1 E-RAB释放次数，ENB由于S1链路故障发起释放'] +\
                              df_drop_top['QCI1 E-RAB释放次数，由于ENB其他异常原因']

df_drop_top['小区拥塞占比'] = (df_drop_top['QCI1 E-RAB释放次数，由于ENB小区拥塞导致的释放'] +
                                 df_drop_top['QCI1 E-RAB释放次数，由于ENB过载控制导致的释放'])\
                                /df_drop_top['掉话总次数']
df_drop_top['无线环境问题占比'] = df_drop_top['QCI1 E-RAB释放次数，由于ENB的无线链路失败']\
                              /df_drop_top['掉话总次数']
df_drop_top['切换失败占比'] = (df_drop_top['QCI1 E-RAB释放次数，由于ENB重建立失败'] +
                               df_drop_top['QCI1 E-RAB释放次数，跨站重建立失败导致的释放'])\
                               /df_drop_top['掉话总次数']
df_drop_top['基站关断或复位占比'] = df_drop_top['QCI1 E-RAB释放次数，由于小区关断或复位']\
                                  /df_drop_top['掉话总次数']
df_drop_top['传输故障占比'] = df_drop_top['QCI1 E-RAB释放次数，ENB由于S1链路故障发起释放'] / df_drop_top['掉话总次数']
df_drop_top['其他原因占比'] = df_drop_top['QCI1 E-RAB释放次数，由于ENB其他异常原因'] / df_drop_top['掉话总次数']

df_drop_top = df_drop_top.sort_values(by=['[LTE]E-RAB建立成功数目(QCI=1)','[FDD]E-RAB掉话率(QCI=1)'],ascending = [False,False]) # 按时间顺序升序排列

df_tmp2  = df_drop_top.iloc[:,18:25] # 只取我们需要的列构建一个零时的表

df_tmp2['问题主要原因'] = df_tmp2.apply(lambda x:findmax(x),axis=1) # 将表按行输入找最大值的函数，得到最大值所在的列的index

df_drop_top['原因分析'] = df_tmp2['问题主要原因']
drop_cause = {'小区拥塞占比':'基站资源拥塞',
               '无线环境问题占比':'无线环境差',
               '切换失败占比':'切换问题',
               '基站关断或复位占比':'基站关断或复位',
               '传输故障占比':'传输故障',
               '其他原因占比':'其他原因(不明)'
}
df_drop_top['原因分析'] = df_drop_top['原因分析'].map(drop_cause)


# =============================================================================
# 输出报表
# =============================================================================
with  pd.ExcelWriter(report_path + 'VOLTE_指标分析(日)_' + KPI_date + '.xlsx')  as writer:  #输出到excel
    book = writer.book
    sheet = book.add_worksheet('全市')
    sheet.insert_image('A2' , pic_path + "全市VOLTE语音接通率.png")
    sheet.insert_image('A23', pic_path + "全市VOLTE掉话率.png")
    sheet.insert_image('A44', pic_path + "全市VOLTE呼叫次数.png")
    sheet.insert_image('A65', pic_path + "全市VOLTE用户数.png")
    sheet.insert_image('A86', pic_path + "全市VOLTE视频接通率.png")
    for name in TOP_country_name:
        sheet = book.add_worksheet(name)
        sheet.insert_image('A2' , pic_path + name + "VOLTE语音接通率.png")
        sheet.insert_image('A23', pic_path + name + "VOLTE掉话率.png")
        sheet.insert_image('A44', pic_path + name + "VOLTE呼叫次数.png")
        sheet.insert_image('A65', pic_path + name + "VOLTE用户数.png")
        sheet.insert_image('A86', pic_path + name + "VOLTE视频接通率.png")

with  pd.ExcelWriter(report_path + 'VOLTE_TOP小区分析(日)_' + KPI_date + '.xlsx')  as writer:  #输出到excel
    df_connect_top.to_excel(writer,'呼叫成功率TOP小区',index = False)
    df_drop_top.to_excel(writer,'掉话率TOP小区',index = False)






