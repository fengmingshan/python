# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-10-16 16:11:15
# @Last Modified by:   Administrator
# @Last Modified time: 2019-10-16 16:13:20

import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


# =============================================================================
# 生成各县退服清单
# =============================================================================
def 填写退服小区(a,b):
	if pd.isnull(a):
		return b.split('_')[0] + '_' + b.split('_')[1]
	else:
		return a

def 填写退服时长(a,b):
	if pd.isnull(a):
		return b
	else:
		return a

def bulid_Index(a,b,c):
    if a == '基站中断':
        return b
    else:
        return c

def fill_Index(a,b,c,d):
    if pd.isnull(a):
        if b == '基站中断':
            return c
        else:
            return d
    else:
        return a

current_date = str(datetime.now()).split('.')[0].split(' ')[0]

data_path = 'D:/_小程序/4G小区退服计算' 
if not os.path.exists(data_path ):
    os.mkdir(data_path)
if not os.path.exists(data_path +'./报表输出'):
    os.mkdir(data_path + './报表输出')
os.chdir(data_path)

exempt_file  = '免责站点.xlsx'
block_cell = '屏蔽小区.xlsx'

df_exempt = pd.read_excel(data_path + exempt_file)
df_eric = pd.read_excel(r'D:\2019年工作\2019年4月小区退服指标计算（新）'+ '\\' + '爱立信基站信息.xlsx' )
df_zte = pd.read_excel(r'D:\2019年工作\2019年4月小区退服指标计算（新）'+ '\\' + '中兴基站信息.xlsx' )
df_eNodeB_info = df_eric.append(df_zte)

all_files = os.listdir(data_path)
break_files = [x for x in all_files if 'alarm_cel_exit_service_child' in x]

df_ALL = pd.DataFrame()
for file in break_files :
    df_tmp = pd.read_excel(data_path + file,skiprows = 1)
    df_ALL= df_ALL.append(df_tmp)
df_ALL = df_ALL.reset_index()
df_ALL.drop('index',axis = 1,inplace = True)

df_LTE = df_ALL[(df_ALL['是否NB小区'] == '否') | (df_ALL['是否NB小区'].isnull() == True) ]

df_LTE['退服小区标识'] = df_LTE.apply(lambda x : 填写退服小区(x.关联小区标识,x.告警对象名称),axis = 1)
#df_LTE['LTE小区个数'] = df_LTE['LTE小区个数'].map(lambda x : 1 if pd.isnull(x) else x)
df_LTE.rename(columns={'退服时长(分钟)':'总退服时长',
                       '告警清除时间':'告警恢复时间',
                       '6-8点退服时长（分钟）':'总6至8点退服时长',
                       '8-22点退服时长（分钟）':'总8至22点退服时长',
                       '22-24点退服时长（分钟）':'总22至24点退服时长',
                       'LTE6-8点退服时长（分钟）':'LTE6至8点退服时长',
                       'LTE8-22点退服时长（分钟）':'LTE8至22点退服时长',
                       'LTE22-24点退服时长（分钟）':'LTE22至24点退服时长'},inplace =True)

df_LTE['LTE退服总时长'] = df_LTE['总退服时长']
df_LTE['LTE6至8点退服时长'] = df_LTE['总6至8点退服时长']
df_LTE['LTE8至22点退服时长'] = df_LTE['总8至22点退服时长']
df_LTE['LTE22至24点退服时长'] = df_LTE['总22至24点退服时长']
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('Heartbeat Failure','基站中断'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('PLMN Service Unavailable','小区退服'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('Service Unavailable','小区退服'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('基站退出服务','基站中断'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('小区不可用告警','小区退服'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('LTE小区退出服务','小区退服'))
df_LTE['告警标题'] = df_LTE['告警标题'].map(lambda x:x.replace('网元断链告警','基站中断'))

df_LTE['Index'] = df_LTE.apply(lambda x :bulid_Index(x.告警标题,x.所属基站ID,x.退服小区标识),axis =1)

df_LTE = pd.merge(df_LTE,df_eNodeB_info,how = 'left' , on = 'Index')

df_LTE['Index'] = df_LTE.apply(lambda x :fill_Index(x.Index,x.告警标题,x.所属基站ID,x.退服小区标识),axis =1)


df_break_times = pd.pivot_table(df_LTE, index=['Index'],
                                        values =['告警对象名称',
                                                 'LTE退服总时长' ],
                                        aggfunc = {'告警对象名称' :'count',
                                                   'LTE退服总时长': np.sum})
df_break_times = df_break_times.reset_index()
df_break_times.rename(columns={'告警对象名称':'本月累计断站次数',
                               'LTE退服总时长':'本月累计退服时长(分钟)'},inplace =True)

df_LTE = pd.merge(df_LTE,df_break_times,how = 'left' , on = 'Index')
df_LTE_remission = df_LTE[['区县','厂家名称','所属基站ID','告警对象名称','中文名称','网元等级','LTE6至8点退服时长','LTE8至22点退服时长','LTE22至24点退服时长']]

df_LTE = df_LTE[['区县','厂家名称','所属基站ID','中文名称','网元等级','告警标题','告警发生时间','告警恢复时间','LTE退服总时长','本月累计退服时长(分钟)','本月累计断站次数',]]


df_LTE_duration = df_LTE.sort_values(by=['本月累计退服时长(分钟)','告警发生时间'],ascending = [False,True]) # 按退服时长降序排列
df_LTE_duration = df_LTE_duration.reset_index().drop('index',axis = 1)
df_LTE_duration = df_LTE_duration[['区县', '厂家名称', '所属基站ID', '中文名称', '网元等级', '告警标题','告警发生时间','告警恢复时间','LTE退服总时长','本月累计退服时长(分钟)','本月累计断站次数' ]]

df_LTE_duration.drop_duplicates('中文名称',keep = 'first' ,inplace = True)
df_LTE_duration = df_LTE_duration[~df_LTE_duration['所属基站ID'].isin(df_exempt['eNodeB_ID'])]
df_LTE_duration = df_LTE_duration[['区县', '厂家名称', '所属基站ID', '中文名称', '网元等级', '告警标题', '本月累计退服时长(分钟)', '本月累计断站次数']]


df_LTE_times = df_LTE.sort_values(by=['本月累计断站次数','告警发生时间'],ascending = [False,True],) # 按退服时长降序排列
df_LTE_times = df_LTE_times[~df_LTE_times['所属基站ID'].isin(df_exempt['eNodeB_ID'])]
df_LTE_times = df_LTE_times[['区县', '厂家名称', '所属基站ID', '中文名称', '网元等级', '告警标题', '本月累计断站次数','本月累计退服时长(分钟)' ]]
df_LTE_times.drop_duplicates('中文名称',keep = 'first' ,inplace = True)
df_LTE_times = df_LTE_times.reset_index().drop('index',axis = 1)


# =============================================================================
# 计算各县累计断站时长(不剔除免责)
# =============================================================================
statistics_file = [x for x in all_files if '小区退服时长统计' in x]
df_statistics = pd.read_excel(data_path + statistics_file[0],skiprows = 3)

df_statistics['A类小区平均退服时长'] = df_statistics['6-8点小区平均退服时长（分钟）'] * 1 + \
                                         df_statistics['8-22点小区平均退服时长（分钟）'] * 1.2 + \
                                         df_statistics['22-24点小区平均退服时长（分钟）'] * 1

df_statistics['B类小区平均退服时长'] = df_statistics['6-8点小区平均退服时长（分钟）.1'] * 1 + \
                                         df_statistics['8-22点小区平均退服时长（分钟）.1'] * 1.2 + \
                                         df_statistics['22-24点小区平均退服时长（分钟）.1'] * 1

df_statistics['CD类退服总时长'] = df_statistics['6-8点退服总时长（分钟）.2'] + \
                                    df_statistics['8-22点退服时长（分钟）.2'] + \
                                    df_statistics['22-24点退服时长（分钟）.2'] + \
                                    df_statistics['6-8点退服总时长（分钟）.3'] + \
                                    df_statistics['8-22点退服时长（分钟）.3'] + \
                                    df_statistics['22-24点退服时长（分钟）.3']
df_statistics['CD类小区总数'] =   df_statistics['C类小区总数'] +  df_statistics['D类小区总数']
df_statistics['CD类小区平均退服时长'] = df_statistics['CD类退服总时长']/df_statistics['CD类小区总数']

df_cell_num = df_statistics.drop_duplicates('地市/区县',keep = 'first' )
df_cell_num = df_cell_num[['地市/区县','A类小区总数','B类小区总数','CD类小区总数']]
df_cell_num.rename(columns={'地市/区县':'区县'},inplace = True)

df_country_break = pd.pivot_table(df_statistics, index=['地市/区县'],
                                              values =['A类小区平均退服时长' ,
                                                       'B类小区平均退服时长',
                                                       'CD类小区平均退服时长',
                                                       'A类小区总数',
                                                       'B类小区总数',
                                                       'CD类小区总数'],
                                              aggfunc = {'A类小区平均退服时长':np.sum,
                                                         'B类小区平均退服时长':np.sum,
                                                         'CD类小区平均退服时长':np.sum,
                                                         'A类小区总数':np.max,
                                                         'B类小区总数':np.max,
                                                         'CD类小区总数':np.max})
df_country_break = df_country_break.reset_index()

df_country_break = df_country_break[['地市/区县','A类小区总数','A类小区平均退服时长','B类小区总数','B类小区平均退服时长','CD类小区总数','CD类小区平均退服时长']]
df_country_break.rename(columns={'A类小区平均退服时长':'A类小区平均退服时长(达标值: <115分钟)',
                                   'B类小区平均退服时长':'B类小区平均退服时长(达标值: <150分钟)',
                                   'CD类小区平均退服时长':'CD类小区平均退服时长(达标值: <300分钟)',},inplace =True)
df_country_break = df_country_break.sort_values(by=['CD类小区总数'],ascending = [True]) # 按退服时长降序排列

# =============================================================================
# 计算各县累计断站时长(剔除免责)
# =============================================================================
df_LTE_remission = df_LTE_remission[~df_LTE_remission['所属基站ID'].isin(df_exempt['eNodeB_ID'])]
df_LTE_remission.fillna(0,inplace = True)

df_remission_classA = df_LTE_remission[df_LTE_remission['网元等级'] == 'A']
df_remission_classB = df_LTE_remission[df_LTE_remission['网元等级'] == 'B']
df_remission_classCD = df_LTE_remission[(df_LTE_remission['网元等级'] == 'C')|(df_LTE_remission['网元等级'] == 'D')]

df_remission_classA['A类小区退服时长'] = df_remission_classA['LTE6至8点退服时长'] * 1 + \
                                         df_remission_classA['LTE8至22点退服时长'] * 1.2 + \
                                         df_remission_classA['LTE22至24点退服时长'] * 1

df_remission_classB['B类小区退服时长'] = df_remission_classB['LTE6至8点退服时长'] * 1 + \
                                         df_remission_classB['LTE8至22点退服时长'] * 1.2 + \
                                         df_remission_classB['LTE22至24点退服时长'] * 1

df_remission_classCD['CD类小区退服时长'] = df_remission_classCD['LTE6至8点退服时长'] * 1 + \
                                         df_remission_classCD['LTE8至22点退服时长'] * 1.2 + \
                                         df_remission_classCD['LTE22至24点退服时长'] * 1

df_country_classA = pd.pivot_table(df_remission_classA, index=['区县'],
                                                        values =['A类小区退服时长'],
                                                        aggfunc = {'A类小区退服时长':np.sum}
)
df_country_classA = df_country_classA.reset_index()

df_country_classB = pd.pivot_table(df_remission_classB, index=['区县'],
                                                        values =['B类小区退服时长'],
                                                        aggfunc = {'B类小区退服时长':np.sum}
)
df_country_classB = df_country_classB.reset_index()

df_country_classCD = pd.pivot_table(df_remission_classCD, index=['区县'],
                                                        values =['CD类小区退服时长'],
                                                        aggfunc = {'CD类小区退服时长':np.sum}
)
df_country_classCD = df_country_classCD.reset_index()

df_country_remission = pd.merge(df_cell_num , df_country_classA , on = '区县' , how = 'left')
df_country_remission = pd.merge(df_country_remission , df_country_classB , on = '区县' , how = 'left')
df_country_remission = pd.merge(df_country_remission , df_country_classCD , on = '区县' , how = 'left')
df_country_remission.fillna(0,inplace = True)
df_country_remission['A类平均退服时长'] = df_country_remission['A类小区退服时长']/df_country_remission['A类小区总数']
df_country_remission['B类平均退服时长'] = df_country_remission['B类小区退服时长']/df_country_remission['B类小区总数']
df_country_remission['CD类平均退服时长'] = df_country_remission['CD类小区退服时长']/df_country_remission['CD类小区总数']
df_country_remission['A类平均退服时长'] = df_country_remission['A类平均退服时长'].map(lambda x:round(x,1))
df_country_remission['B类平均退服时长'] = df_country_remission['B类平均退服时长'].map(lambda x:round(x,1))
df_country_remission['CD类平均退服时长'] = df_country_remission['CD类平均退服时长'].map(lambda x:round(x,1))
df_country_remission = df_country_remission[['区县','A类小区总数','A类平均退服时长','B类小区总数','B类平均退服时长','CD类小区总数','CD类平均退服时长',]]

# =============================================================================
# 输出结果
# =============================================================================
with  pd.ExcelWriter(out_path  + '全市小区退服汇总_' +  current_date + '.xlsx')  as writer:  #输出到excel
    df_country_remission.to_excel(writer,'全市小区退服时长(剔除免责)',index=False)
    df_country_break.to_excel(writer,'全市小区退服时长(原始)',index=False)
    df_LTE_duration.head(50).to_excel(writer,'全市退服时长TOP50',index=False)
    df_LTE_times.head(50).to_excel(writer,'全市退服次数TOP50',index=False)

for name in ['沾益县', '会泽县', '罗平县', '宣威市', '麒麟区', '马龙县', '富源县', '陆良县', '师宗县']:
    df_break_duration = df_LTE_duration[df_LTE_duration['区县'] == name]
    df_break_times = df_LTE_times[df_LTE_times['区县'] == name]
    with  pd.ExcelWriter('./报表输出' + name + '_' + '小区退服清单_' +  current_date + '.xlsx')  as writer:  #输出到excel
        df_break_duration.to_excel(writer, name + '退服时长排序', index = False)
        df_break_times.to_excel(writer, name + '退服次数排序', index = False)