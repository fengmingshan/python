# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 10:36:01 2018
拆分诊断命令
@author: Administrator
"""

data_path = r'D:\制作诊断脚本' + '\\'

vol_cmd_ommb1 = 'CMD_OMMB1.txt'
SCTP_cmd_ommb1 = '查询SCTP脚本_ommb1.txt'

vol_cmd_ommb2 = 'CMD_OMMB2.txt'
SCTP_cmd_ommb2 = '查询SCTP脚本_ommb2.txt'

# =============================================================================
# 拆分ommb1 的cmd 
# =============================================================================
vol_file = open(data_path + vol_cmd_ommb1,encoding ='utf-8' ) 
vol_lines = vol_file.readlines()

sctp_file = open(data_path + SCTP_cmd_ommb1,encoding ='utf-8' )
sctp_lines = sctp_file.readlines()

for i in range(0,int(len(sctp_lines)/105) + 1,1):
    with open(data_path + 'B2CMD' + str(i+1) + '.txt','a',encoding ='utf-8' ) as f:
        if i <  int(len(sctp_lines)/105) :
            for j in range(i*105,(i+1)*105,1):
                f.write(vol_lines[j]) 
                f.write(sctp_lines[j]) 
        else:
            for j in range(i*105,len(vol_lines),1):
                f.write(vol_lines[j]) 
            for k in range(i*105,len(sctp_lines),1):
                f.write(sctp_lines[k]) 

# =============================================================================
# 拆分ommb2 的cmd 
# =============================================================================       
vol_file = open(data_path + vol_cmd_ommb2,encoding ='utf-8' ) 
vol_lines = vol_file.readlines()

sctp_file = open(data_path + SCTP_cmd_ommb2,encoding ='utf-8' )
sctp_lines = sctp_file.readlines()

for i in range(0,int(len(sctp_lines)/114) + 1,1):
    with open(data_path + 'B2CMD' + str(i+1) + '.txt','a',encoding ='utf-8' ) as f:
        if i <  int(len(sctp_lines)/114) :
            for j in range(i*114,(i+1)*114,1):
                f.write(vol_lines[j]) 
                f.write(sctp_lines[j]) 
        else:
            for j in range(i*114,len(vol_lines),1):
                f.write(vol_lines[j]) 
            for k in range(i*114,len(sctp_lines),1):
                f.write(sctp_lines[k]) 

        
        
    