# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 13:21:05 2018

@author: Administrator
"""
import pandas as pd 
import os

path = r'd:\2018年工作\2018年4月CQI专项\原始数据' + '\\'
outpath = r'd:\2018年工作\2018年4月CQI专项' + '\\'
PhyChannel1 = 'PhyChannel_ommb1.xlsx' 
PhyChannel2 = 'PhyChannel_OMMB2.xlsx'
cell_name = 'cell_name.xlsx'

df_chan1 =  pd.read_excel(outpath + PhyChannel1 ,encoding='utf-8',skiprows=1)
df_chan2 =  pd.read_excel(outpath + PhyChannel2 ,encoding='utf-8',skiprows=1)
df_chan1 = df_chan1.drop([0,1])
df_chan2 = df_chan2.drop([0,1])
df_chan = df_chan1.append(df_chan2)
df_chan = df_chan[['管理网元ID','对象描述','UE CQI/PMI上报周期配置(毫秒)(小区复位生效)']]
df_chan['对象描述'] = df_chan['对象描述'].map(lambda x:x.split('=')[1])
df_chan['管理网元ID'] = df_chan['管理网元ID'] + '_' + df_chan['对象描述']
del df_chan['对象描述']
df_chan = df_chan.rename(columns={'管理网元ID': 'cell_id'})
df_chan = df_chan.reset_index()
del df_chan['index']


files = os.listdir(path)
df_result = pd.DataFrame(columns=[])
df_day =  pd.read_excel(outpath + cell_name , encoding='utf-8')

for file in files:
    df_tmp = pd.read_csv(path + file ,engine= 'python',encoding='gbk')
    df_tmp['CQI1-6求和'] = df_tmp['12.2 CQI0上报数量(次)'] +  df_tmp['12.2 CQI1上报数量(次)'] +  df_tmp['12.2 CQI2上报数量(次)'] +  df_tmp['12.2 CQI3上报数量(次)'] +  df_tmp['12.2 CQI4上报数量(次)'] +  df_tmp['12.2 CQI5上报数量(次)']+  df_tmp['12.2 CQI6上报数量(次)'] 
    df_day_tmp = df_tmp[['小区名称','时间','CQI1-6求和','12.2 CQI上报总数量(次)']]
    df_day_tmp['优良率'] = 1 - df_day_tmp['CQI1-6求和']/ df_day_tmp['12.2 CQI上报总数量(次)']
    df_day = pd.merge(df_day,df_day_tmp,how='left', on='小区名称' )
    df_result = df_result.append(df_tmp)
    df_result['优良率'] = 1 - df_result['CQI1-6求和']/ df_result['12.2 CQI上报总数量(次)']

    
# =============================================================================
# 质优小区
# =============================================================================
df_zte_good = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']>0.88)]    
df_zte_good = df_zte_good.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].mean()  
df_zte_good['优良率'] = 1 - df_zte_good['CQI1-6求和']/ df_zte_good['12.2 CQI上报总数量(次)']
df_zte_good.loc['合计'] = df_zte_good.apply(lambda x: x.sum()) 
df_zte_good['质差贡献比重'] = ''
for i in range(0,len(df_zte_good)-1,1):
    df_zte_good.loc[i,'质差贡献比重'] = df_zte_good.loc[i,'CQI1-6求和']/df_zte_good.loc['合计','CQI1-6求和']
df_zte_good.loc['合计','小区名称'] = '合计'
df_zte_good.loc['合计','质差贡献比重'] = 0
df_zte_good['CQI1-6求和'] = df_zte_good['CQI1-6求和'].map(lambda x:round(x,0))
df_zte_good['12.2 CQI上报总数量(次)'] = df_zte_good['12.2 CQI上报总数量(次)'].map(lambda x:round(x,0))
df_zte_good['优良率'] = df_zte_good['优良率'].map(lambda x:round(x,4))
df_zte_good['质差贡献比重'] = df_zte_good['质差贡献比重'].map(lambda x:round(x,5))
df_zte_good = df_zte_good.sort_values(by='质差贡献比重',ascending = False) # 按质差贡献比重降序排列 
df_zte_good = df_zte_good.drop('合计')
df_zte_good['cell_id'] = df_zte_good['小区名称'].map(lambda x: x.split('_')[0] +'_'+ x.split('_')[1])
df_zte_good = pd.merge(df_zte_good,df_chan,how = 'left',on = 'cell_id'  )

# =============================================================================
# 质差小区
# =============================================================================
df_zte_worse = df_result[(df_result['厂家']=='中兴')&(df_result['优良率']<0.88)]    
df_zte_worse = df_zte_worse.groupby(by='小区名称',as_index=False)[['基站名称','12.2 CQI上报总数量(次)','CQI1-6求和']].mean()  
df_zte_worse['优良率'] = 1 - df_zte_worse['CQI1-6求和']/ df_zte_worse['12.2 CQI上报总数量(次)']
df_zte_worse.loc['合计'] = df_zte_worse.apply(lambda x: x.sum()) 
df_zte_worse['质差贡献比重'] = ''
for i in range(0,len(df_zte_worse)-1,1):
    df_zte_worse.loc[i,'质差贡献比重'] = df_zte_worse.loc[i,'CQI1-6求和']/df_zte_worse.loc['合计','CQI1-6求和']
df_zte_worse.loc['合计','小区名称'] = '合计'
df_zte_worse.loc['合计','质差贡献比重'] = 0
df_zte_worse['CQI1-6求和'] = df_zte_worse['CQI1-6求和'].map(lambda x:round(x,0))
df_zte_worse['12.2 CQI上报总数量(次)'] = df_zte_worse['12.2 CQI上报总数量(次)'].map(lambda x:round(x,0))
df_zte_worse['优良率'] = df_zte_worse['优良率'].map(lambda x:round(x,4))
df_zte_worse['质差贡献比重'] = df_zte_worse['质差贡献比重'].map(lambda x:round(x,5))
df_zte_worse = df_zte_worse.sort_values(by='质差贡献比重',ascending = False) # 按质差贡献比重降序排列
df_zte_worse = df_zte_worse.drop('合计')
df_zte_worse['cell_id'] = df_zte_worse['小区名称'].map(lambda x: x.split('_')[0] +'_'+ x.split('_')[1])
df_zte_worse = pd.merge(df_zte_worse,df_chan,how = 'left',on = 'cell_id'  )

with pd.ExcelWriter(outpath + '中兴质差.xlsx') as writer: 
    df_day.to_excel(writer,'按天汇总') 
    df_zte_worse.to_excel(writer,'中兴质差扇区') 
    df_zte_good.to_excel(writer,'中兴优良扇区') 
    df_chan.to_excel(writer,'CQI周期配置') 


