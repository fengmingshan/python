# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:06:25 2019

@author: Administrator
"""
import pandas as pd
import os
import numpy as np

L1800_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,49, 50, 51, 52, 53, 54, 55, 56, 129, 130, 131, 132, 133, 134, 135, 136,177, 178, 179, 180, 181, 182]
L800_list = [17, 18, 19, 20, 21, 22,145, 146, 147, 148, 149,150]
title_list = ['DATE_ID',
              'HOUR_ID',
              'eNodeB',
              'EUTRANCELLFDD',
              'Acc_Wireless ConnSucRate(%)',
              'Acc_ERAB_dropping rate (%)',
              'Air Interface_Traffic_Volume_UL_MBytes',
              'Air Interface_Traffic_Volume_DL_MBytes',
              'Int_Downlink Latency (ms)',
              'Max number of UE in RRc', 'DL_Util_of_PRB',
              'pmCellDowntimeAuto1', 'pmCellDowntimeMan1', 'Data_Coverage',
              'Ava_CellAvail (%)', 'Num of LTE Redirect to 3G',
              'Avg Number of UL Active Users', 'Avg Number of DL Active Users',
              'Avg User Fell Throughput (Mbps)']

data_path = r'd:\_小程序\超忙小区分析' + '\\'



