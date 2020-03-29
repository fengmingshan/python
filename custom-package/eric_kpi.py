# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:29:49 2020

@author: Administrator
"""

import pandas as pd
import numpy as np


def eric_KPI_modify_dtyps(df):
    df['DATE_ID'] = df['DATE_ID'].map(lambda x:x.replace('\'',''))
    df['eNodeB'] = df['eNodeB'].map(lambda x:int(x.replace('\'','')))
    return df

def eric_KPI_rename(df):
    df.rename(columns={"RRC连接重建比例_1": "RRC连接重建比例",
                       "UE上下文掉线率_1": "UE上下文掉线率",
                       "RAB掉线率_1": "RAB掉线率",
                       "S1接口切换成功率_1": "S1接口切换成功率",
                       "系统内切换成功率_1": "系统内切换成功率",
                       "LTE重定向到3G的次数_1": "LTE重定向到3G的次数",
                       "空口上行用户面流量（MByte）_1": "上行流量_MB",
                       "空口下行用户面流量（MByte）_1477070755617-11": "下行流量_MB",
                       "分QCI用户体验上行平均速率（Mbps）_1": "上行体验速率_Mbps",
                       "分QCI用户体验下行平均速率（Mbps）_1": "下行体验流量_Mbps",
                       "空口下行用户面丢包率_1": "空口下行用户面丢包率",
                       "上行PRB平均占用率_1": "上行PRB平均占用率",
                       "下行PRB平均占用率_1": "下行PRB平均占用率",
                       "PDCCH信道CCE占用率_1": "PDCCH信道CCE占用率",
                       "PRACH信道占用率_1": "PRACH信道占用率",
                       "非竞争 Preamble占用率_1": "非竞争Preamble占用率",
                       "寻呼信道占用率_1": "寻呼信道占用率",
                       "最大RRC连接用户数_1": "最大RRC连接用户数",
                       "平均RRC连接用户数_1": "平均RRC连接用户数",
                       "上行平均激活用户数_1": "上行平均激活用户数",
                       "下行平均激活用户数_1": "下行平均激活用户数",
                       "平均激活用户数_1": "平均激活用户数",
                       "最大激活用户数_1": "最大激活用户数",
                       "CQI优良比(>=7比例)": "CQI优良比",
                       }, inplace = True
    )
    return df

