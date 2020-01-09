# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 14:18:41 2020

@author: Administrator
"""
import pandas as pd
import os

path = 'D:/2020年工作/2020年1月春节返乡用户分析'
os.chdir(path)

df = pd.read_excel('./曲靖返乡用户v1.xlsx')
df.rename(columns = {'小区':'CID'},inplace = True)
df['CID'] = df['CID'].map(lambda x:int(str(x)[6:]))

df_cell_info = pd.read_excel('./物理站址与支局对应清单.xlsx')
df_cell_info['eNodeB'] = df_cell_info['小区号'].map(lambda x:int(x.split('_')[0]))
df_cell_info['cell'] = df_cell_info['小区号'].map(lambda x:int(x.split('_')[1]))
df_cell_info['CID'] =df_cell_info['eNodeB']*256 + df_cell_info['cell']
df_user = pd.merge(df,df_cell_info,how = 'left', on = 'CID')
df_user = df_user[~df_user['支局'].isnull()]
df_user.sort_values(by=['手机号','7天内占用小区次数'], ascending=[True,False], inplace=True)  # 按时间顺序升序排列

#df_missing =  df_user[df_user.支局.isnull()]
#with pd.ExcelWriter('./缺失小区.xlsx') as writer:
#    df_missing.to_excel(writer,index =False)
df_home = pd.DataFrame()
users = list(set(df_user.手机号))
for i,user in enumerate(users):
    df_tmp = df_user[df_user['手机号'] == user]
    df_tmp.reset_index(inplace = True,drop =True)
    user_home_location = df2.loc[0,:]
    df_home = df_home.append(user_home_location)
    if len(users) != 0 and len(users)%100 == 0:
        print('Total {all} users,finished {cur} uesrs,{per}% percent of the total!'.format(all = len(users),cur = i,per = i/len(users)*100))
