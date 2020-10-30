# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 08:41:41 2020

@author: Administrator
"""

'''
APPLY CMRIGHT:SYSTEM={system};
ADD 1X_LINKCELL_L:POS="399"-"{cellid}"-"{ncell_pn}",NCELLSYSTEM={nell_sys},NCELL={nell},ISEACHOTHER=0;
ADD 1X_NGHBRLIST_L:POS="399"-"{cellid}"-"0"-"{ncell_pn}",NCELLSYSTEM={nell_sys},NCELL={nell},NGHBR_CONFIG=0,SEARCH_PRIORITY=0,ACCESS_ENTRY_HO=Enable,FREQ_INCL=NOT_INC,ACCESS_HO_ALLOWED=Enable,TIMING_INCL=NOT_INC,NGHBR_TX_OFFSET=0,NGHBR_TX_DURATION=3,NGHBR_TX_PERIOD=0,ADD_PILOT_REC_INCL=NOT_INC,NGHBR_PILOT_REC_TYPE=0,SRCH_OFFSET_NGHBR=0;
'''

import pandas as pd
import os
import pandas

path = r'D:\_python小程序\制作添加3G小区及载频邻区'
os.chdir(path)

cell_files = [x for x in os.listdir() if 'cell' in x ]
carrier_files = [x for x in os.listdir() if 'carrier' in x ]

S_CELL_SYSTEM = '399'


cell_name = ['col','col1','col2','col3','ci','pn','lac','null1','bts','bts_name','cellid','null2','cellname','null3','null4','null5','null6','null7']
carriern_name = ['bts','btsname','cellid','cellname','pn','distance','handovercount','handoversucc','null','istwo_way','islocked','userlabel']
for cellfile, carrierfile in zip(cell_files,carrier_files):
    cell = cellfile.split('.')[0][-1]
    df_cell = pd.read_csv(cellfile, names = cell_name,delimiter= '\t',encoding = 'gbk')
    df_carrier = pd.read_csv(carrierfile, names = carriern_name,delimiter= '\t',encoding = 'gbk')
    with open('./脚本输出/add_neighbor_cell{}.txt'.format(cell),'w') as f:
        line_apply_rights = 'APPLY CMRIGHT:SYSTEM={system};'.format(system = S_CELL_SYSTEM)
        f.writelines(line_apply_rights + '\n')
        for i in range(len(df_cell)):
            line_add_cell_nei = 'ADD 1X_LINKCELL_L:POS="{system}"-"{cellid}"-"{ncell_pn}",NCELLSYSTEM={nell_sys},NCELL={ncell},ISEACHOTHER=0;'.format(
                system=S_CELL_SYSTEM,
                cellid=cell,
                ncell_pn = df_cell.loc[i,'pn'],
                nell_sys= df_cell.loc[i,'bts'],
                ncell= df_cell.loc[i,'cellid'],
            )
            f.writelines(line_add_cell_nei + '\n')

        for i in range(len(df_carrier)):
            line_add_carrier_nei = 'ADD 1X_NGHBRLIST_L:POS="{system}"-"{cellid}"-"0"-"{ncell_pn}",NCELLSYSTEM={nell_sys},NCELL={nell},NGHBR_CONFIG=0,SEARCH_PRIORITY=0,ACCESS_ENTRY_HO=Enable,FREQ_INCL=NOT_INC,ACCESS_HO_ALLOWED=Enable,TIMING_INCL=NOT_INC,NGHBR_TX_OFFSET=0,NGHBR_TX_DURATION=3,NGHBR_TX_PERIOD=0,ADD_PILOT_REC_INCL=NOT_INC,NGHBR_PILOT_REC_TYPE=0,SRCH_OFFSET_NGHBR=0;'.format(
                system =S_CELL_SYSTEM,
                cellid=cell,
                ncell_pn = df_carrier.loc[i,'pn'],
                nell_sys = df_carrier.loc[i,'bts'],
                nell = df_carrier.loc[i,'cellid'],
            )
            f.writelines(line_add_carrier_nei + '\n')



