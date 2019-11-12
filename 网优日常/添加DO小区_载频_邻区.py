import os
import pandas as pd

data_path = 'D:/Test/制作添加DO小区脚本'
os.chdir(data_path)

#df_cell = pd.read_excel('.xls')

with open('add_DO_cell.txt', 'w') as f:
    line_apply_right = 'APPLY CMRIGHT:SYSTEM = {bts};'.format(bts=)
    f.write(line1 + '\n')
    
    line_add_cell= 'ADD DO_CELL:POS="{bts}"-"{cell}",PHYCELLID={phycell},PILOTPN={pn},SUBNETINDEXID={subnet},SECTORID="00a8c0006e800000ac18cd2e16{sectorid}",LOCALTIMEOFFSET=GMT+08:00 Beijing,ALIAS_B="cellname",MS_IPL_SUP_IND_A=0,ENCRYPT_MODE_A=0,PILOTINCREMENT=3,SCENETYPE=2;'.format(bts=, cell=, phycell=, pn=, subnet=, sectorid=)
    f.write(line_add_cell + '\n')

    line_add_carrier = 'ADD DO_CARRIER:POS="{bts}"-"{cell}"-"{carrier}",GROUPID=1,RFSSUBSYSTEM={rfsys},LINKPATH=1,TRXID={trx},AUXRFSSUBSYSTEM=255,AUXLINKPATH=255,AUXTRXID=255;'.format(bts=, cell=, carrier=, rfsys=, trx=)
    f.write(line_add_carrier + '\n')
    
    line_add_nb = 'ADD DO_NGHBRLIST_L:POS="{bts}"-"{cell}"-"{carrier}",NBANID={anid},NBSYSTEM={nbsys},NBCELLID={nbcll},NBCARRIERID={nbcarrier},ISEACHOTHER=YES,SEARCHWINDOWSIZE=10CHIP,SEARCHWINDOWOFFSET=0,FPDCHSUPPORTED=NOT_SUPPORTED;'.format(bts=, cell=, carrier=, anid=, nbsys=, nbcll=, nbcarrier=)
    f.write(line_add_nb + '\n')
    
    line_release_right = 'RELEASE CMRIGHT:SYSTEM = {bts};'.format(bts=)
    f.write(line_release_right + '\n')
