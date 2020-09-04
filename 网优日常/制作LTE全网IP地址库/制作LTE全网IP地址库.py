# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:24:43 2020

@author: Administrator
"""

'''
原始数据
爱立信导出全网IP地址:txt格式
爱立信导出全网IP地址:txt格式
中兴3个OMMB管理网元(NEManagedElement)表导出:xlsx格式
'''

import pandas as pd
import os
from IPy import IP
from math import log

path = r'D:\_python小程序\制作LTE全网IP地址库'
os.chdir(path)


def calc_gateway(ip):
    if '6.49.' in ip:
        mask = 25
    else:
        mask = 26
    ip_net = IPy.IP(ip + '/'+str(mask),make_net=True)
    return '.'.join(str(IPy.IP.net(ip_net)).split('.')[:-1]) +\
            '.' +str(int(str(IPy.IP.net(ip_net)).split('.')[-1])+1)


def calc_mask(mask_str):
    ip4 = int(mask_str.split('.')[3])
    num = int(log(ip4,2))
    mask_num = 24 + (8 - num)
    return mask_num


files = os.listdir()
eric_file = [x for x in files if '爱立信' in x][0]
zte_files = [x for x in files if 'NEManagedElement' in x]
hw_file =  [x for x in files if '华为' in x][0]

# 处理爱立信IP
df_eric = pd.DataFrame(columns = ['name','manu','ip','gateway','mask'])
name = []
ip = []
with open(eric_file,'r') as f:
    content = f.readlines()
    content = content[4:]
    for line in content:
        name.append(line.strip().split('\t')[0])
        ip.append(line.strip().split('\t')[2])
df_eric['name'] = name
df_eric['ip'] = ip
df_eric['manu'] = '爱立信'
df_eric['mask'] = df_eric['ip'].map(lambda x:25 if '6.49.' in x else 26)
df_eric['gateway'] = df_eric['ip'].map(lambda x:calc_gateway(x))

# 处理中兴IP
df_zte_list = []
for file in zte_files:
    df_zte_tmp = pd.DataFrame(columns = ['name','manu','ip','gateway','mask'])

    df_tmp = pd.read_excel(file,sheet_name = 'NEManagedElement')
    df_tmp.drop([0,1,2],axis =0,inplace =True)
    df_tmp.reset_index(inplace =True,drop=True)
    df_zte_tmp['name'] = df_tmp['USERLABEL']
    df_zte_tmp['manu'] = '中兴'
    df_zte_tmp['ip'] = df_tmp['MEADDR']
    df_zte_tmp['mask'] = df_zte_tmp['ip'].map(lambda x:25 if '6.49.' in x else 26)
    df_zte_tmp['gateway'] = df_zte_tmp['ip'].map(lambda x:calc_gateway(x))
    df_zte_list.append(df_zte_tmp)
df_zte = pd.concat(df_zte_list,axis = 0 )

# 处理华为IP
df_hw = pd.DataFrame(columns = ['name','manu','ip','gateway','mask'])
name = []
ip = []
mask = []
with open(hw_file,'r') as f:
    content = f.readlines()
    for i,line in enumerate(content):
        if 'LST OMCH:;' in line:
            if 'DBS3900' in content[i+1]:
                name.append(content[i+1].strip())
            if '本端IP地址' in content[i+10]:
                ip.append(content[i+10].strip().split('=')[1])
            if '本端子网掩码' in content[i+11]:
                mask.append(content[i+11].strip().split('=')[1])
df_hw['name'] = name
df_hw['ip'] = ip
df_hw['manu'] = '华为'
df_hw['mask'] = mask
df_hw['gateway'] = df_hw['ip'].map(lambda x:calc_gateway(x))
df_hw['mask'] = df_hw['mask'].map(lambda x:calc_mask(x))

df_all = pd.concat([df_eric,df_zte,df_hw],axis = 0)

with open('全网IP汇总.csv','w',newline = '') as f:
    df_all.to_csv(f,index =False)