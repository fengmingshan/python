# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 19:35:41 2018

@author: Administrator
"""
import pandas as pd
from pandas import DataFrame
#==============================================================================
# 打开excel表格
#==============================================================================
file=r'D:\test\BTS.xls' 
file2=r'D:\test\BTS.csv'
df1=pd.read_excel(file,dtype =str,encoding='utf-8') 
df2=pd.read_excel(file,skiprows=1,dtype =str,encoding='utf-8')  # skiprows=1跳过1行
df3=pd.read_excel(file,sheetname='Sheet2',dtype =str,encoding='utf-8') # sheetname='sheet1'指定读取得sheet名

df4=pd.read_csv(file2,dtype =str,encoding='gbk') 

#==============================================================================
# 单元格的选取.loc与.iloc与.at
#==============================================================================
file=r'D:\test\BTS.xls'
df1 = pd.read_excel(file,dtype =str,encoding='utf-8') 
df1.loc[1,'BTS']
df1.loc[1,'Cell']
df1.loc[0:2]    #选取表1的1-3行
df1.loc[:,'Cell']  #选取表的Cell列，所有行
df2=pd.DataFrame()
df1['BTS']
df2['BTS']=''
df2['BTS']=df1['BTS']

df1 = df1.set_index('BTS')
df1 = df1.reset_index()

df1.loc[1,'Cell']  #当行索引不是数字的时候，.loc就必须带行的名字，这样写就报错了
df1.loc['[83]BS8800_QJ富源后所杨家坟_WDTL_ZCT','Cell'] 
 
df1.iloc[0,0] 
df1.iloc[1,1]
df1.iloc[:,0]
df1.iloc[0:3,:]

df1.loc[0,'区县']='富源'  #.loc可以选择不存在的列直接赋值，.iloc不行
df1.loc[1,'区县']='大河'
for i in range(0,len(df1),1):
    df1.loc[i,'区县']=df1.loc[i,'BTS'].split('_')[1][2:4]        
df1.at[0,'BTS']
df1.at[2,'Cell']

df1.iat[0,0]
df1.iat[2,0]

#==============================================================================
# 筛选 
#==============================================================================
file=r'D:\test\3G话务量.xls'
df1 = pd.read_excel(file,dtype =str,encoding='utf-8') 

df1['DO最大用户数']=df1['DO最大用户数'].replace('-',0)
df1['DO前向吞吐量(kbps)']=df1['DO前向吞吐量(kbps)'].replace('-',0)

df1['呼叫话务量(Erl)']=df1['呼叫话务量(Erl)'].astype(float)
df1['DO最大用户数']=df1['DO最大用户数'].astype(float)

df2 = df2[df2['小区名称'].isin(df_cell['小区名称'])]    # 可以筛选包含在某个表某一列中的项目
df1 = df1[df1['小区名称'].isin(df2['小区名称']) ]


df2=df1[df1['呼叫话务量(Erl)']>5] 
df3=df1[['Cell','呼叫话务量(Erl)']][df1['呼叫话务量(Erl)']>5] 
df4=df1[(df1['呼叫话务量(Erl)']>5)&(df1['DO最大用户数']>20)] 
df5=df1[(df1['呼叫话务量(Erl)']>5)|(df1['DO最大用户数']>20)] 
df6=df1['Cell'][(df1['呼叫话务量(Erl)']>5)|(df1['DO最大用户数']>20)] 
df7=df1[['Cell','呼叫话务量(Erl)','DO最大用户数']][(df1['呼叫话务量(Erl)']>5)&(df1['DO最大用户数']>20)] 

# =============================================================================
# 切片
# =============================================================================
df2['区县'] = df2['小区名称'].split('_')[0:2] #可以直接对整列切片，然后复制给新建的列

# =============================================================================
# 排序 ：默认升序，ascending = False 降序
# =============================================================================
df1 = df1.sort_values(by='呼叫话务量(Erl)',ascending = True) # 按时间顺序升序排列  
df1 = df1.sort_values(by='DO最大用户数',ascending = False) # 按时间顺序降序排列  
df1 = df1.sort_index(axis = 0,ascending = True)     # 按行号升序排列  
df1 = df1.sort_index(axis = 1,ascending = True)     # 按列名进行升序排列  
df1 = df1.sort_values(by=['DO最大用户数','DO最大用户数'],ascending = False) # 按多个索引降序排序 

# =============================================================================
# 行列重命名
# =============================================================================
df1.rename(columns={'呼叫话务量(Erl)':'话务量','DO最大用户数':'DO用户数'},inplace =True)

#==============================================================================
#  融合表格Merge=vlookup
#==============================================================================
file1=r'D:\test\1X话务量-2.xls'
df1 = pd.read_excel(file1,dtype =str,encoding='utf-8') 

file2=r'D:\test\DO话务量-2.xls'
df2 = pd.read_excel(file2,dtype =str,encoding='utf-8') 

df3=pd.merge(df1,df2,how='left',on='Cell')

df4=pd.merge(df1,df2,how='right',on='Cell')

df5=pd.merge(df1,df2,how='left',on='Cell')

df6=pd.merge(df1,df2,how='inner',on='Cell')

#==============================================================================
# 简单透视Groupby()
#==============================================================================
file1=r'D:\test\3G话务量-2.xls'
df1 = pd.read_excel(file1,dtype =str,encoding='utf-8') 
df1['呼叫话务量(Erl)']=df1['呼叫话务量(Erl)'].astype(float)
df1['软切换比例']=df1['软切换比例'].astype(float)
df1['DO最大用户数']=df1['DO最大用户数'].astype(float)
df1['DO前向吞吐量(kbps)']=df1['DO前向吞吐量(kbps)'].astype(float)

df2 =df1.groupby(by='BTS',as_index=False).sum()
df3 =df1.groupby(by='BTS').sum()
df4 =df1.groupby(by='BTS')[['呼叫话务量(Erl)','DO最大用户数']].sum()
df4 =df1.groupby(by='BTS',as_index=False)[['呼叫话务量(Erl)','DO最大用户数']].sum()

#==============================================================================
# map & lambda 函数
#==============================================================================
file1=r'D:\test\123.xls'
df1 = pd.read_excel(file1,dtype =str,encoding='utf-8') 
df1['告警对象名称']=df1['告警对象名称'].map(lambda x:x.replace('工程调测-',''))
df1['告警对象名称']=df1['告警对象名称'].map(lambda x:x.replace('调测-',''))
df1['告警对象名称']=df1['告警对象名称'].map(lambda x:x.replace('调测_',''))
    
lis2=list(x+2 for x in lis1)

foo = [1, 2, 3, 4, 5]
map(lambda x: x + 10, foo)
map(lambda x: x*2, foo)
list(map(lambda x: x + 10, foo))
list(map(lambda x: x*2, foo))
print(list(map(lambda x: x + 10, foo)))
print(list(map(lambda x: x*2, foo)))

#map到字典
df2 = DataFrame({'员工':['冯明山','孙家雄','郭晴阳','解艳刚']})
dict_job = {'冯明山':'网络分析','孙家雄':'系统优化','郭晴阳':'网络测试','解艳刚':'现场优化'} 
df2['员工'] = df2['员工'].map(dict_job)


#==============================================================================
# 分列
#==============================================================================
file1=r'D:\test\BTS.xls'
df1 = pd.read_excel(file,dtype =str,encoding='utf-8') 
df1['col1'],df1['col2'],df1['col3'],df1['col4']= zip(*df1['BTS'].map(lambda x: x.split('_')))

df1['区县']=''
for i in range(0,len(df1),1):
    df1.loc[i,'区县']=df1.loc[i,'BTS'].split('_')[1]    
df1['区县']=df1['区县'].map(lambda x:x[2:4])

#zip()函数的用法
list1 = [1, 2, 3]
list2 = [4,5,6]
tuple1 = zip(list1,list2)
zipped = list(tuple1)
tuple2 = zip(*zipped)
unzip = list(tuple2)

#==============================================================================
# 写入到excel表格，to_excel没有追加写入模式，会覆盖表格原来的内容，to_csv有追加写入模式
#==============================================================================
writer = pd.ExcelWriter('output.xlsx')
df1.to_excel(writer,'Sheet1') 
df2.to_excel(writer,'Sheet2',index=False) # index=False不带row index输出
writer.save()
writer.close()

writer = pd.ExcelWriter(r'd:\test\output.xls')
df7.to_excel(writer,'123') 
df1.to_excel(writer,'456') 
df2.to_excel(writer,'sheet1') 

df1.to_excel(writer,'Sheet1',startrow=5,sol=5) # 可以将两个df写入到一个sheet，指定写入的起始位置


df_sum.to_csv(r'd:\data\计算结果.csv')
df_cell_num.to_csv(r'd:\data\计算结果.csv',mode='a') # to_csv有追加写入模式不会覆盖原来的内容
help(DataFrame.to_csv)

# 但是上面的写法还是很麻烦，输出一个文件要写4行代码：最后还要save，close
# Pythonic的写法是：
with pd.ExcelWriter('output.xlsx') as writer: #不用保存和退出，系统自动会完成
    df1.to_excel(writer,'Sheet1') 
    df2.to_excel(writer,'Sheet2',index=False) # index=False不带row index输出
