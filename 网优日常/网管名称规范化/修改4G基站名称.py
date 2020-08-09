# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:38:15 2020

@author: Administrator
"""

import pandas as pd
import os

path =r'D:\_python小程序\网管名称规范化'
os.chdir(path)

files =os.listdir()
files

df_4g_enb = pd.read_excel('4g_change_name.xlsx',sheet_name = 'bts_name')
df_4g_enb.columns

df_ommb1 = df_4g_enb[(df_4g_enb['SubNetwork']== 530301)|
    (df_4g_enb['SubNetwork']==874001)
]

df_ommb2 = df_4g_enb[(df_4g_enb['SubNetwork']== 530303)|
    (df_4g_enb['SubNetwork']==530306)|
    (df_4g_enb['SubNetwork']==530307)|
    (df_4g_enb['SubNetwork']==530308)|
    (df_4g_enb['SubNetwork']==874009)|
    (df_4g_enb['SubNetwork']==874003)|
    (df_4g_enb['SubNetwork']==874006)|
    (df_4g_enb['SubNetwork']==874007)|
    (df_4g_enb['SubNetwork']==874008)|
    (df_4g_enb['SubNetwork']==874009)
]

df_ommb3 = df_4g_enb[(df_4g_enb['SubNetwork']== 530302)|
    (df_4g_enb['SubNetwork']==530304)|
    (df_4g_enb['SubNetwork']==530305)|
    (df_4g_enb['SubNetwork']==874002)|
    (df_4g_enb['SubNetwork']==874004)|
    (df_4g_enb['SubNetwork']==874005)
]

df_ommb1.reset_index(drop = True, inplace = True)
df_ommb2.reset_index(drop = True, inplace = True)
df_ommb3.reset_index(drop = True, inplace = True)

def make_cmd(df,ommb):
    apply_rights_cmd = []
    change_name_cmd1 = []
    change_name_cmd2 = []

    for i in range(0,len(df)):
        apply_right_line ='APPLY MUTEXRIGHT:SUBNET="{subnet}",NE="{enb}";'.format(
                subnet = df.loc[i,'SubNetwork'],
                enb = df.loc[i,'MEID'],
                )
        change_line1 = 'UPDATE:MOC="NEManagedElement",MOI="SubNetwork={subnet},MEID={enb}",ATTRIBUTES="USERLABEL={name}",EXTENDS="";'.format(
            subnet = df.loc[i,'SubNetwork'],
            enb = df.loc[i,'MEID'],
            name = df.loc[i,'new_name'],
            )
        change_line2 = 'UPDATE:MOC="ENBFunctionFDD",MOI="SubNetwork={subnet},MEID={enb},ENBFunctionFDD={enb}",ATTRIBUTES="userLabel={name}",EXTENDS="";'.format(
            subnet = df.loc[i,'SubNetwork'],
            enb = df.loc[i,'MEID'],
            name = df.loc[i,'new_name'],
                )
        apply_rights_cmd.append(apply_right_line)
        change_name_cmd1.append(change_line1)
        change_name_cmd2.append(change_line2)

    with open('./脚本输出/修改4G基站名称_{ommb}.txt'.format(ommb = ommb),'w') as f:
        for line in apply_rights_cmd:
             f.writelines(line+ '\n')

        f.writelines('\n')

        for line1,line2 in zip(change_name_cmd1,change_name_cmd2):
             f.writelines(line1 + '\n')
             f.writelines(line2 + '\n')


make_cmd(df_ommb1,'OMMB1')
make_cmd(df_ommb2,'OMMB2')
make_cmd(df_ommb3,'OMMB3')
