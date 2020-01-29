import os
import pandas as pd

data_path = 'D:/Test/制作添加DO小区脚本'
os.chdir(data_path)

df_DO_CELL_info = pd.read_excel('add_carrier.xlsx')
for i in range(len(df_DO_CELL_info)):
    bts = df_DO_CELL_info.loc[i,'system']
    cell = df_DO_CELL_info.loc[i,'cellid']
    phycell = df_DO_CELL_info.loc[i,'phycellid']
    carrier = df_DO_CELL_info.loc[i,'carrierid']
    rfsys = df_DO_CELL_info.loc[i,'rfssubsystem']
    trx = df_DO_CELL_info.loc[i,'trxid']
    pn = df_DO_CELL_info.loc[i,'PN']
    subnet = df_DO_CELL_info.loc[i,'SUB_NET']
    sectorid = df_DO_CELL_info.loc[i,'SECTORID']
    cellname = df_DO_CELL_info.loc[i,'CELL_NAME']

    with open('./脚本输出/add_DO_cell.txt', 'a') as f:
        line_apply_right = 'APPLY CMRIGHT:SYSTEM = {bts};'.format(bts = bts)
        f.write(line_apply_right + '\n')

        line_add_cell= 'ADD DO_CELL:POS="{bts}"-"{cell}",PHYCELLID={phycell},PILOTPN={pn},SUBNETINDEXID={subnet},SECTORID="{sectorid}",LOCALTIMEOFFSET=GMT+08:00 Beijing,ALIAS_B="{cellname}",MS_IPL_SUP_IND_A=0,ENCRYPT_MODE_A=0,PILOTINCREMENT=3,SCENETYPE=2;'.format(bts = bts, cell = cell, phycell = phycell, pn = pn, subnet = subnet, sectorid = sectorid,cellname = cellname)
        f.write(line_add_cell + '\n')

        line_add_carrier = 'ADD DO_CARRIER:POS="{bts}"-"{cell}"-"{carrier}",GROUPID=1,RFSSUBSYSTEM={rfsys},LINKPATH=1,TRXID={trx},AUXRFSSUBSYSTEM=255,AUXLINKPATH=255,AUXTRXID=255;'.format(bts = bts, cell = cell, carrier = carrier, rfsys = rfsys, trx = trx)
        f.write(line_add_carrier + '\n')

        line_release_right = 'RELEASE CMRIGHT:SYSTEM = {bts};'.format(bts = bts)
        f.write(line_release_right + '\n')

        f.write('\n')

