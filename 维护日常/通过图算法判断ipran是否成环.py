# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 17:13:06 2020

@author: Administrator
"""

import pandas as pd
import os
import numpy as np
import difflib


path = r'D:\_python小程序\通过ipran端口数据判断相邻节点'
port_file = 'ipran_全网端口描述.xls'
equipment_file = 'ipran_equipment.xls'
bts_file = 'ipran_bts.xls'

os.chdir(path)

#处理全网基站业务数据，统计全网A设备下挂基站数量
df_bts = pd.read_excel(bts_file)
df_bts.columns
df_bts = df_bts.groupby(by = '归属A名称',as_index=False)['基站类型'].count()
bts_num_dict = df_bts.set_index('归属A名称')['基站类型'].to_dict()

df_port = pd.read_excel(port_file)
df_port.columns

# 处理设备清单数据，生成从编码到A设备以及A设备到编码的字典：
df_equipment = pd.read_excel(equipment_file)
host2equip_dict = df_equipment[['主机名','设备名称']].set_index('主机名')['设备名称'].to_dict()
equip_list = list(df_port['设备名称'].unique())
equip_dict = {k:v for k,v in enumerate(equip_list)}
reverse_equip_dict = {v:k for k,v in enumerate(equip_list)}

# 处理全网端口数据
df_port_has_describe = df_port[~df_port.端口描述.isnull()&df_port['端口描述'].str.contains('MCN.')]
has_describe_list = list(df_port_has_describe.设备名称.unique())
without_describe_list = [x for x in equip_list if x not in has_describe_list]

df_port_has_describe['端口描述'][df_port_has_describe['端口描述'] == 'N-QJ-LL-YTLNHDZX-A-1.MCN.ATN910I'] = 'YN-QJ-LL-YTLNHDZX-A-1.MCN.ATN910I'

for string in ['dT:', 'dt:', 'uT:', 'ut:', 'pT:', 'uP:', 'uT锛颰:', 'TO:', 'TO-', '<']:
    df_port_has_describe['端口描述'] = df_port_has_describe['端口描述'].map(lambda x:x.replace(string,''))
df_port_has_describe['端口描述'] = df_port_has_describe['端口描述'].map(lambda x:x.replace('pTYN','YN'))
df_port_has_describe['端口描述'] = df_port_has_describe['端口描述'].map(lambda x:x.replace('YYN','YN'))
df_port_has_describe['端口描述'] = df_port_has_describe['端口描述'].map(lambda x:x.replace(':YN','YN'))
df_port_has_describe['端口描述'] = df_port_has_describe['端口描述'].map(lambda x:x.strip())

def handle_port_descirbe(x):
    if x.startswith('YN') and '-GigabitEthernet' in x:
        return x.split('-GigabitEthernet')[0]
    elif x.startswith('YN') and '-GE' in x:
        return x.split('-GE')[0]
    elif x.startswith('YN'):
        return x.split(':')[0]
    elif '(N/A)' in x:
        return x.split('(N/A)')[0]
    else:
        return x.split(':')[0]

df_port_has_describe['相邻主机名'] = df_port_has_describe['端口描述'].map(lambda x:handle_port_descirbe(x))
df_port_has_describe['相邻主机名'] = df_port_has_describe['相邻主机名'].map(lambda x:x.replace(':',''))
df_port_has_describe['相邻主机名'] = df_port_has_describe['相邻主机名'].map(lambda x:x.replace(',','.'))

df_port_has_describe.reset_index(drop =True, inplace =True)
df_port_has_describe['相邻主机名'] = df_port_has_describe['相邻主机名'].map(
    lambda x:x if x in list(df_equipment['主机名'].unique()) else difflib.get_close_matches(x,list(df_equipment['主机名'].unique()), n=1)[0]
)

#df_port_wrong = df_port_has_describe[~df_port_has_describe['相邻主机名'].isin(list(df_equipment['主机名'].unique())) ]
df_port_right = df_port_has_describe[df_port_has_describe['相邻主机名'].isin(list(df_equipment['主机名'].unique())) ]
df_port_right['相邻A设备名称'] = df_port_right['相邻主机名'].map(host2equip_dict)
df_port_right['相邻A设备id'] = df_port_right['相邻A设备名称'].map(reverse_equip_dict)
df_port_right['设备id'] = df_port_right['设备名称'].map(reverse_equip_dict)
df_port_right['下挂基站数'] = df_port_right['设备名称'].map(bts_num_dict)
df_port_right['相邻A设备下挂基站数'] = df_port_right['相邻A设备名称'].map(bts_num_dict)
df_port_right = df_port_right[~df_port_right['相邻A设备id'].isnull()]
df_port_right = df_port_right[['设备名称', '设备id','下挂基站数','相邻A设备名称', '相邻A设备id', '相邻A设备下挂基站数']]

equipment_list = list(df_port_right['设备id'].unique())
neighbor_bts_num_list = []
for equip in equipment_list:
    df_tmp = df_port_right[df_port_right['设备id']==equip]
    df_num_tmp = df_tmp.groupby(by = '设备名称',as_index =False)[['相邻A设备名称','相邻A设备下挂基站数']].agg({'相邻A设备名称':len,'相邻A设备下挂基站数':np.sum})
    neighbor_bts_num_list.append(df_num_tmp)
df_num = pd.concat(neighbor_bts_num_list, axis = 0)
df_num.rename(columns ={
    '相邻A设备名称':'关联A设备数量',
    '相邻A设备下挂基站数':'关联基站数量',
    },inplace =True
)
df_port_right = pd.merge(df_port_right, df_num, how ='left', on = '设备名称')
df_port_right['关联基站总数'] = df_port_right['下挂基站数'] + df_port_right['关联基站数量']
