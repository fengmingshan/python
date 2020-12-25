import pandas as pd
import os

path = 'C:/Users/Administrator/Desktop/新建文件夹'

files = os.listdir(path)
os.chdir(path)

li1 = []
for f in files:
    df = pd.read_excel(f,sheet_name = '全部基站清单',skiprows = 2)
    li1.append(df)

df_all = pd.concat(li1,axis = 0)
df_all.columns
df_erl = df_all.groupby(by= '物理站址')['本周语音话务量（erl）\t'].mean().reset_index()

with pd.ExcelWriter('语音话务量.xls') as f:
    df_erl.to_excel(f,index =False)
