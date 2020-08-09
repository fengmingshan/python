# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:16:54 2020

@author: Administrator
"""

import pandas as pd
import os

path = r'D:\_python小程序\网管名称规范化'
os.chdir(path)
files = os.listdir()

df_3g = pd.read_excel('3G配置数据汇总.xlsx')
columns = list(df_3g.columns)

df_4g = pd.read_excel('4G配置数据汇总.xlsx')
columns2 = list(df_4g.columns)

df_4g_enb = pd.read_excel('4G_eNodeB汇总.xlsx')
columns3 = list(df_4g_enb.columns)


df_3g_res = df_3g[(df_3g['btsalias'].str.contains('公安'))
    |(df_3g['btsalias'].str.contains('武警'))
    |(df_3g['btsalias'].str.contains('政府'))
    |(df_3g['btsalias'].str.contains('人大'))
    |(df_3g['btsalias'].str.contains('党校'))
    |(df_3g['btsalias'].str.contains('政协'))
    |(df_3g['btsalias'].str.contains('部队'))
    |(df_3g['btsalias'].str.contains('飞机'))
    |(df_3g['btsalias'].str.contains('机场'))
    |(df_3g['btsalias'].str.contains('驻地'))
    |(df_3g['btsalias'].str.contains('雷达'))
    |(df_3g['alias_b'].str.contains('公安'))
    |(df_3g['alias_b'].str.contains('武警'))
    |(df_3g['alias_b'].str.contains('政府'))
    |(df_3g['alias_b'].str.contains('人大'))
    |(df_3g['alias_b'].str.contains('党校'))
    |(df_3g['alias_b'].str.contains('政协'))
    |(df_3g['alias_b'].str.contains('部队'))
    |(df_3g['alias_b'].str.contains('飞机'))
    |(df_3g['alias_b'].str.contains('机场'))
    |(df_3g['alias_b'].str.contains('驻地'))
    |(df_3g['alias_b'].str.contains('雷达'))
    ]

df_4g_res = df_4g[(df_4g['userLabel'].str.contains('公安'))
    |(df_4g['userLabel'].str.contains('武警'))
    |(df_4g['userLabel'].str.contains('政府'))
    |(df_4g['userLabel'].str.contains('人大'))
    |(df_4g['userLabel'].str.contains('党校'))
    |(df_4g['userLabel'].str.contains('政协'))
    |(df_4g['userLabel'].str.contains('部队'))
    |(df_4g['userLabel'].str.contains('飞机'))
    |(df_4g['userLabel'].str.contains('机场'))
    |(df_4g['userLabel'].str.contains('驻地'))
    |(df_4g['userLabel'].str.contains('雷达'))
    ]

df_4g_enbres = df_4g_enb[(df_4g_enb['USERLABEL'].str.contains('公安'))
    |(df_4g_enb['USERLABEL'].str.contains('武警'))
    |(df_4g_enb['USERLABEL'].str.contains('政府'))
    |(df_4g_enb['USERLABEL'].str.contains('人大'))
    |(df_4g_enb['USERLABEL'].str.contains('党校'))
    |(df_4g_enb['USERLABEL'].str.contains('政协'))
    |(df_4g_enb['USERLABEL'].str.contains('部队'))
    |(df_4g_enb['USERLABEL'].str.contains('飞机'))
    |(df_4g_enb['USERLABEL'].str.contains('机场'))
    |(df_4g_enb['USERLABEL'].str.contains('驻地'))
    |(df_4g_enb['USERLABEL'].str.contains('雷达'))
    ]


with pd.ExcelWriter(r'C:\Users\Administrator\Desktop\网管名称规范化\3g不规范.xlsx') as f:
    df_3g_res.to_excel(f,index =False)

with pd.ExcelWriter(r'C:\Users\Administrator\Desktop\网管名称规范化\4g小区不规范.xlsx') as f:
    df_4g_res.to_excel(f,index =False)

with pd.ExcelWriter(r'C:\Users\Administrator\Desktop\网管名称规范化\4g_基站名称不规范.xlsx') as f:
    df_4g_enbres.to_excel(f,index =False)
