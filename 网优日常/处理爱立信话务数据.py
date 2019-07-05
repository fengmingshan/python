import pandas as pd
import numpy as np
import os

path =  r'D:\_非标带宽扩容'+'\\'
out_path = r'D:\_非标带宽扩容\结果输出' +'\\'
eric_file = '爱立信6月话务量.csv'
title = '标题.xlsx'

df_title =  pd.read_excel(path + title ,encoding = 'utf-8')
titles = list(df_title.columns)
df_eric = pd.read_csv(path + eric_file,engine = 'python',header = None,names = df_title.columns)
df_eric = df_eric.fillna(0)
df_eric['eNodeB'] = df_eric['eNodeB'].map(lambda x:x.replace('\'',''))
df_eric['DATE_ID'] = df_eric['DATE_ID'].map(lambda x:x.replace('\'',''))
df_eric['EUTRANCELLFDD'] = df_eric['EUTRANCELLFDD'].map(lambda x:x.replace('\'',''))
df_eric['Acc_Wireless ConnSucRate(%)'] = df_eric['Acc_Wireless ConnSucRate(%)'].astype(float)
df_eric['Acc_ERAB_dropping rate (%)'] = df_eric['Acc_ERAB_dropping rate (%)'].astype(float)
df_eric['Air Interface_Traffic_Volume_UL_MBytes'] = df_eric['Air Interface_Traffic_Volume_UL_MBytes'].astype(float)
df_eric['Air Interface_Traffic_Volume_DL_MBytes'] = df_eric['Air Interface_Traffic_Volume_DL_MBytes'].astype(float)
df_eric['Int_Downlink Latency (ms)'] = df_eric['Int_Downlink Latency (ms)'].astype(float)
df_eric['Max number of UE in RRc'] = df_eric['Max number of UE in RRc'].astype(int)
df_eric['DL_Util_of_PRB'] = df_eric['DL_Util_of_PRB'].astype(float)
df_eric['pmCellDowntimeAuto1'] = df_eric['pmCellDowntimeAuto1'].astype(int)
df_eric['pmCellDowntimeMan1'] = df_eric['pmCellDowntimeMan1'].astype(int)
df_eric['Data_Coverage'] = df_eric['Data_Coverage'].astype(int)
df_eric['Ava_CellAvail (%)'] = df_eric['Ava_CellAvail (%)'].astype(int)
df_eric['Num of LTE Redirect to 3G'] = df_eric['Num of LTE Redirect to 3G'].astype(int)
df_eric['Avg Number of UL Active Users'] = df_eric['Avg Number of UL Active Users'].astype(float)
df_eric['Avg Number of DL Active Users'] = df_eric['Avg Number of DL Active Users'].astype(float)
df_eric['Avg User Fell Throughput (Mbps)'] = df_eric['Avg User Fell Throughput (Mbps)'].astype(float)


df_eric_pivot = pd.pivot_table(df_eric, index=['eNodeB','DATE_ID','EUTRANCELLFDD'],
                                  values =['Max number of UE in RRc' ,
                                           'DL_Util_of_PRB',
                                           'Air Interface_Traffic_Volume_UL_MBytes',
                                           'Air Interface_Traffic_Volume_DL_MBytes'],
                                  aggfunc = {'Max number of UE in RRc':np.max,
                                             'DL_Util_of_PRB':np.max,
                                             'Air Interface_Traffic_Volume_UL_MBytes':np.max,
                                             'Air Interface_Traffic_Volume_DL_MBytes':np.max})
df_eric_pivot['Traffic_Volume_MBytes'] = (df_eric_pivot['Air Interface_Traffic_Volume_UL_MBytes'] + \
                                           df_eric_pivot['Air Interface_Traffic_Volume_DL_MBytes'])/1024


df_eric_pivot = df_eric_pivot.reset_index()
df_eric_busy  = df_eric_pivot[((df_eric_pivot['DL_Util_of_PRB']>= 0.5) & (df_eric_pivot['Traffic_Volume_MBytes']>= 1.5))
                              |((df_eric_pivot['DL_Util_of_PRB']>= 0.5) & (df_eric_pivot['Max number of UE in RRc']>= 50))]
df_eric_busy['上月超忙天数'] = df_eric_busy['EUTRANCELLFDD'].value_counts
busy_counts = df_eric_busy['EUTRANCELLFDD'].value_counts()
dict_busy = busy_counts.to_dict()
df_eric_busy['上月超忙天数']  = df_eric_busy['EUTRANCELLFDD'].map(dict_busy)

with pd.ExcelWriter(out_path + '爱立信汇总.xlsx') as writer:
     df_eric_busy.to_excel(writer,'超忙小区',index =False)
     df_eric_pivot.to_excel(writer,'原始数据',index =False)


