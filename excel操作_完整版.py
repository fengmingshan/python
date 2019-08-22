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

# 读取超大文件需要分块读取
reader  = pd.read_csv(path + file , engine = 'python', iterator=True)
     loop = True
     chunkSize = 10000
     chunks = []
     while loop:
          try:
               chunk = reader.get_chunk(chunkSize)
               chunks.append(chunk)
          except StopIteration:
               loop = False
               print("Iteration is stopped.")
     df_tmp = pd.concat(chunks, ignore_index=True)

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
# 切片,分列
# =============================================================================
df1 = pd.DataFrame({
    '小区名称' : ['宣威_板桥', '陆良_板桥', '罗平_板桥', '宣威_热水', '会泽_田坝', '会泽_迤车'],
    'col3': [0, 1, 9, 4, 2, 3],
})

df1['区县'] = df1['小区名称'].str[0:2]  #可以直接对整列切片，然后复制给新建的列

# =============================================================================
# 排序 ：默认升序，ascending = False 降序
# =============================================================================
df1 = pd.DataFrame({
    'col1' : ['A', 'A', 'B', np.nan, 'D', 'C'],
    'col2' : [2, 1, 9, 8, 7, 4],
    'col3': [0, 1, 9, 4, 2, 3],
})
df1.sort_values(by='col1',ascending = True,inplace = True) # 按时间顺序升序排列
df1.sort_values(by='col1', ascending=False, na_position='first',inplace = True)
df1.sort_values(by='col1', ascending=False, na_position='last',inplace = True)

df2 = df1.sort_values(by='col2',ascending = False,inplace = True) # 按时间顺序降序排列
df3= df1.sort_index(axis = 0,ascending = True,inplace = True)     # 按行号升序排列
df4 = df1.sort_index(axis = 1,ascending = True,inplace = True)     # 按列名进行升序排列
df5 = df1.sort_values(by=['col1','col2'],ascending = [False,False]) # 按多个索引降序排序

# =============================================================================
# 行列重命名
# =============================================================================
df1 = pd.DataFrame({
    'col1' : ['A', 'A', 'B', np.nan, 'D', 'C'],
    'col2' : [2, 1, 9, 8, 7, 4],
    'col3': [0, 1, 9, 4, 2, 3],
})

df1.rename(columns={'col1':'话务量',
                    'col2':'DO用户数'
                    'col3':'DO流量'
                    },inplace =True)

# =============================================================================
# 删除行列
# =============================================================================
df1 = df1.drop([0,1,2])  # 删除前3行
del df1['编号']  # 删除 '编号'一列

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

# =============================================================================
# 去重复
# =============================================================================
df1.drop_duplicates('eNodeB', keep='first', inplace = True)
help(df1.drop_duplicates)
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

# =============================================================================
# 数据透视表
# =============================================================================
df_yunnan_pivot = pd.pivot_table(df_yunnan, index=['区域'],
                                  values =['CQI上报总次数' ,'CQI大于等于7次数'],
                                  aggfunc = {'CQI上报总次数':np.sum,'CQI大于等于7次数':np.sum})


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

# =============================================================================
# 把字符串转为时间
# =============================================================================
df_3g_traffic['日期'] = pd.to_datetime(df_3g_traffic['日期'])
df_3g_traffic = df_3g_traffic.sort_values(by='日期',ascending = True)
df_3g_traffic['日期'] =  df_3g_traffic['日期'].map(lambda x:str(x))
df_3g_traffic['日期'] =  df_3g_traffic['日期'].map(lambda x:x.split(' ')[0])



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

df_sum.to_csv(r'd:\data\计算结果.csv')
df_cell_num.to_csv(r'd:\data\计算结果.csv',mode='a') # to_csv有追加写入模式不会覆盖原来的内容

# 但是上面的写法还是很麻烦，输出一个文件要写4行代码：最后还要save，close
# Pythonic的写法是：
with pd.ExcelWriter('output.xlsx') as writer: #不用保存和退出，系统自动会完成
    df1.to_excel(writer,'Sheet1')
    df2.to_excel(writer,'Sheet2',index=False) # index=False不带row index输出

with open(data_path + '全网layer规划.xlsx','w') as  writer:
     df_cell.to_csv(writer,index = False)


# 通过多列的数据计算生成一个新的列：
def Judge_MOD3(a,b,c,d): # 定义计算函数
	if a%3 == b % 3  and d-c <= 3:
		return 1
	else:
		return 0
# 使用apply函数将表格的多列输入到Judge_MOD3进行计算，得到一个新的列
df_all['Neighbor1_IS_MOD3'] = df_all.apply(lambda x:Judge_MOD3(x.ServingCell_PCI,x.Neighbor1_PCI,x.Neighbor1_RSRP,x.ServingCell_RSRP),axis =1 )
