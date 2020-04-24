# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 09:39:36 2020

@author: Administrator
"""
import pandas as pd
import os
import numpy
from tqdm import tqdm
from math import sin, cos, asin, sqrt, radians


work_path = 'D:/2020年工作/2020年4月4G邻区专项优化'
if not os.path.exists('./结果输出'):
    os.mkdir('./结果输出')
os.chdir(work_path)


def calc_Distance(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(
        radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance, 0)
    return distance


def judge_neighbor_type(relations):

    L800_list = [17, 18, 19, 20, 21, 22,145, 146, 147, 148, 149,150]
    L1800_list = [49, 50, 51, 52, 53, 54, 55, 56,177, 178, 179, 180, 181, 182]
    L2100_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,129, 130, 131, 132, 133, 134, 135, 136]
    if int(relations.split('-')[0].split('_')[1]) in L1800_list:
        if int(relations.split('-')[1].split('_')[1]) in L1800_list:
            return 'same_frq'
        else:
            return 'diff_frq'
    elif int(relations.split('-')[0].split('_')[1]) in L800_list:
        if int(relations.split('-')[1].split('_')[1]) in L800_list:
            return 'same_frq'
        else:
            return 'diff_frq'
    else:
        if int(relations.split('-')[1].split('_')[1]) in L2100_list:
            return 'same_frq'
        else:
            return 'diff_frq'


list_df = [pd.read_excel('./全网切换关系/' + file, header=5) for file in os.listdir('./全网切换关系')]
df = pd.concat(list_df, axis=0)
df['Scell'] = df['网元'].map(str) + '_' + df['小区'].map(str)
df['Ncell'] = df['邻区关系'].map(lambda x: x.split(':')[3] + '_' + x.split(':')[4])
df['relations'] = df['Scell'] + '-' + df['Ncell']
df['neib_type'] = df['relations'].map(lambda x:judge_neighbor_type(x))
df.set_index('relations', inplace=True)
dict_HandReq = df['系统内每相邻关系切换出请求次数'].to_dict()
dict_HandOutSucc = df['切换出成功次数'].to_dict()
dict_HandInSucc = df['切换入成功次数'].to_dict()
df.reset_index(inplace=True)


#df_1800 = pd.read_excel('./曲靖电信LTE1.8G工参20200421.xls',sheet_name = 'CXT')
#df_1800.drop(['是否边界'],axis = 1, inplace = True)
#df_800 = pd.read_excel('./曲靖电信LTE800M工参20200421.xls',sheet_name = 'CXT')
#df_800.drop(['是否共C网', '是非边界', '逻辑根'],axis = 1, inplace = True)
#df_bts = df_1800.append(df_800)
#df_bts['cell_index'] = df_bts['ENODEBID'].map(str) + '_' +df_bts['CELLID'].map(str)
#df_bts.set_index('cell_index',inplace = True)
#name_dict = df_bts['CELLNAME'].to_dict()
#with open('name_dict.txt','w') as f:
#    f.write(str(name_dict))

with open('name_dict.txt', 'r') as f:
    name_dict = eval(f.read())

#lonlat_dict = {k:(x,y) for k,x,y in zip(df_bts.index, df_bts['LONC'], df_bts['LATC'])}
# with open('lonlat_dict.txt','w') as f:
#    f.write(str(lonlat_dict))

with open('lonlat_dict.txt', 'r') as f:
    lonlat_dict = eval(f.read())


df_cur_config = pd.read_excel('./全网已配置邻区_简.xlsx', enging='python')
df_cur_config['Scell'] = df_cur_config['MEID'].map(str) + '_' + df_cur_config['CellId'].map(str)
df_cur_config['Ncell'] = df_cur_config['eNBId'].map(str) + '_' + df_cur_config['NCellId'].map(str)
df_cur_config['relations'] = df_cur_config['Scell'] + '-' + df_cur_config['Ncell']
df_cur_config = df_cur_config[df_cur_config['relations'].isin(df['relations'])]
df_cur_config['Scell_name'] = df_cur_config['Scell'].map(name_dict)
df_cur_config['Scell_lon'] = df_cur_config['Scell'].map(lambda x: lonlat_dict.get(x, (0, 0))[1])
df_cur_config['Scell_lat'] = df_cur_config['Scell'].map(lambda x: lonlat_dict.get(x, (0, 0))[1])
df_cur_config['Ncell_name'] = df_cur_config['Ncell'].map(name_dict)
df_cur_config['Ncell_lon'] = df_cur_config['Ncell'].map(lambda x: lonlat_dict.get(x, (0, 0))[1])
df_cur_config['Ncell_lat'] = df_cur_config['Ncell'].map(lambda x: lonlat_dict.get(x, (0, 0))[1])
df_miss_info = pd.DataFrame({'cell_index':df_cur_config['Scell'][pd.isnull(df_cur_config['Scell_name'])].unique()})

df_cur_config = df_cur_config[df_cur_config['Scell_lon'] != 0]
df_cur_config['distance'] = df_cur_config.apply(
    lambda x: calc_Distance(
        x.Scell_lon,
        x.Scell_lat,
        x.Ncell_lon,
        x.Ncell_lat),
    axis=1)
df_cur_config['HandReq'] = df_cur_config['relations'].map(dict_HandReq)
df_cur_config['HandOutSucc'] = df_cur_config['relations'].map(dict_HandOutSucc)
df_cur_config['HandInSucc'] = df_cur_config['relations'].map(dict_HandInSucc)
df_cur_config['neib_type'] = df_cur_config['relations'].map(lambda x:judge_neighbor_type(x))
df_cur_config = df_cur_config[[
    'Scell_name',
    'Ncell_name',
    'distance',
    'HandReq',
    'HandOutSucc',
    'HandInSucc',
    'neib_type',
    'Scell',
    'Ncell',
    'relations',
    'Scell_lon',
    'Scell_lat',
    'Ncell_lon',
    'Ncell_lat']]


df_not_configured = df[~df['relations'].isin(df_cur_config['relations'])]
df_not_configured.rename(columns={
    '小区名称': 'Scell_name',
    '系统内每相邻关系切换出请求次数': 'HandReq',
    '切换出成功次数': 'HandOutSucc',
    '切换入成功次数': 'HandInSucc',
}, inplace=True
)
df_not_configured['Scell_lon'] = df_not_configured['Scell'].map(
    lambda x: lonlat_dict.get(x, (0, 0))[1])
df_not_configured['Scell_lat'] = df_not_configured['Scell'].map(
    lambda x: lonlat_dict.get(x, (0, 0))[1])
df_not_configured['Ncell_name'] = df_not_configured['Ncell'].map(name_dict)
df_not_configured['Ncell_lon'] = df_not_configured['Ncell'].map(
    lambda x: lonlat_dict.get(x, (0, 0))[1])
df_not_configured['Ncell_lat'] = df_not_configured['Ncell'].map(
    lambda x: lonlat_dict.get(x, (0, 0))[1])
df_not_configured = df_not_configured[df_not_configured['Scell_lon'] != 0]
df_not_configured['distance'] = df_not_configured.apply(
    lambda x: calc_Distance(
        x.Scell_lon,
        x.Scell_lat,
        x.Ncell_lon,
        x.Ncell_lat),
    axis=1)
df_not_configured['HandReq'] = df_not_configured['relations'].map(dict_HandReq)
df_not_configured['HandOutSucc'] = df_not_configured['relations'].map(dict_HandOutSucc)
df_not_configured['HandInSucc'] = df_not_configured['relations'].map(dict_HandInSucc)
df_not_configured = df_not_configured[[
    'Scell_name',
    'Ncell_name',
    'distance',
    'HandReq',
    'HandOutSucc',
    'HandInSucc',
    'neib_type',
    'Scell',
    'Ncell',
    'relations',
    'Scell_lon',
    'Scell_lat',
    'Ncell_lon',
    'Ncell_lat']]

df_zero_handover = df_cur_config[df_cur_config['HandOutSucc'] <10]
df_zero_handover = df_zero_handover[[
    'Scell_name',
    'Ncell_name',
    'distance',
    'HandReq',
    'HandOutSucc',
    'HandInSucc',
    'neib_type',
    'Scell',
    'Ncell',
    'relations',
    'Scell_lon',
    'Scell_lat',
    'Ncell_lon',
    'Ncell_lat']]

df_neighbor_all = df_cur_config.append(df_not_configured)
df_neighbor_all[df_not_configured['HandOutSucc'] >=10]
df_neighbor_all.reset_index(inplace =True, drop = True)
df_neighbor_all.sort_values(by = 'HandOutSucc',ascending = False, inplace =True)

add_list_same = []
add_list_diff = []
drop_list_same = []
drop_list_diff = []
need2add_list_same = []
need2add_list_diff = []
for cell in tqdm(set(df_neighbor_all['Scell'])):
    df_cell_old_same = df_cur_config[(df_cur_config['Scell']==cell)&(df_cur_config['neib_type']=='same_frq')]
    df_cell_new_same = df_neighbor_all[(df_neighbor_all['Scell']==cell)&(df_neighbor_all['neib_type']=='same_frq')]
    df_cell_old_diff = df_cur_config[(df_cur_config['Scell']==cell)&(df_cur_config['neib_type']=='diff_frq')]
    df_cell_new_diff = df_neighbor_all[(df_neighbor_all['Scell']==cell)&(df_neighbor_all['neib_type']=='diff_frq')]
    if len(df_cell_new_same)>=60:
        df_new_same = df_cell_new_same.iloc[:60,:]
        df_need2add_same = df_cell_new_same.iloc[60:,:]
    else:
        df_new_same = df_cell_new_same
        df_need2add_same = pd.DataFrame(columns = df_neighbor_all.columns)
    df_add_same = df_new_same[~df_new_same['relations'].isin(df_cell_old_same['relations'])]
    df_drop_same = df_cell_old_same[~df_cell_old_same['relations'].isin(df_new_same['relations'])]
    if len(df_cell_new_diff)>=60:
        df_new_diff = df_cell_new_diff.iloc[:60,:]
        df_need2add_diff = df_cell_new_diff.iloc[60:,:]
    else:
        df_new_diff = df_cell_new_diff
        df_need2add_diff = pd.DataFrame(columns = df_neighbor_all.columns)
    df_add_diff = df_new_diff[~df_new_diff['relations'].isin(df_cell_old_diff['relations'])]
    df_drop_diff = df_cell_old_diff[~df_cell_old_diff['relations'].isin(df_new_diff['relations'])]

    add_list_same.append(df_add_same)
    add_list_diff.append(df_add_diff)
    drop_list_same.append(df_drop_same)
    drop_list_diff.append(df_drop_diff)
    need2add_list_same.append(df_need2add_same)
    need2add_list_diff.append(df_need2add_diff)

df_add = pd.concat(add_list_same + add_list_diff, axis =0)
df_drop = pd.concat(drop_list_same + drop_list_diff, axis =0)
df_need2add = pd.concat(need2add_list_same + need2add_list_diff, axis =0)

with pd.ExcelWriter('./结果输出/待添加邻区.xlsx') as f:
    df_add.to_excel(f, '待添加邻区', index=False)

with pd.ExcelWriter('./结果输出/有切换需瘦身邻区对.xlsx') as f:
    df_drop.to_excel(f, '有切换需瘦身邻区对', index=False)

with pd.ExcelWriter('./结果输出/邻区表满无法添加的邻区.xlsx') as f:
    df_need2add.to_excel(f, '邻区表满无法添加的邻区', index=False)

with pd.ExcelWriter('./结果输出/网优工参基础信息缺失.xlsx') as f:
    df_miss_info.to_excel(f, '网优工参无信息', index=False)

with pd.ExcelWriter('./结果输出/无切换可删除邻区对.xlsx') as f:
    df_zero_handover.to_excel(f, '无切换可删除邻区对', index=False)
