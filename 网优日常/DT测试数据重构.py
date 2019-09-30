# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2019-09-25 08:34:51
# @Last Modified by:   Administrator
# @Last Modified time: 2019-09-26 10:15:52

import pandas as pd
import math
from numpy import NaN

path = 'D:/_小程序/DT测试数据重构'

DT_file = '曲靖DT数据.csv'

os.chdir(path)


def judge_mod3(serving_pci, serving_rsrp, neighbor_pci, neighbor_rsrp):
    if neighbor_pci:
        if int(serving_pci) % 3 ==  int(neighbor_pci) % 3:
            delta_rsrp = math.ceil(int(neighbor_rsrp) - int(serving_rsrp))
            return delta_rsrp


df_DT = pd.read_csv(DT_file, engine='python')

for i in range(len(df_DT)):
    mod3_list = []
    for j in range(1, 9):
        mod3_res = judge_mod3(df_DT.loc[i, 'ServingCell_PCI'], df_DT.loc[i, 'ServingCell_RSRP'],
                              df_DT.loc[i, 'Neighbor%d_PCI' % j], df_DT.loc[i, 'Neighbor%d_RSRP' % j])
        mod3_list.append(mod3_res)
    df_DT.loc[i, 'mod3'] = mod3_list
