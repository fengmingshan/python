# -*- coding: utf-8 -*-

import pandas as pd
import os
from pandas import ExcelWriter,DataFrame
from os import listdir
from datetime import datetime
import re
from re import findall

data_path = r'd:\_小程序\爱立信告警统计' + '\\'

def trans_AlarmUnit(df):
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('SubNetwork=QuJing',''))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('SubNetwork=ONRM_ROOT_MO',''))

    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('ENodeBFunction=1',''))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('Cabinet=1',''))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('Equipment=1',''))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('Equipment=1',''))
    df['告警单元'] = df['告警单元'].map(lambda x:x.strip())
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('ManagedElement=','基站:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('EUtranCellFDD=','小区:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('FanGroup=','风扇单元:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('FieldReplaceableUnit=SUP','电源模块'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('Lm=1 CapacityState=CXC4010608 GracePeriod=CXC4010608','无'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('AntennaNearUnit=','天线端口:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('RetSubUnit=','电调单元:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('AntennaUnitGroup=','天线:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('AntennaNearUnit=','天线:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('FieldReplaceableUnit=RRU-','RRU:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('RfPort=','RRU发射端口:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('RiLink=','BBU光口:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('AntennaNearUnit=','天线:'))
    df['告警单元'] = df['告警单元'].map(lambda x:x.replace('NbIotCell=','NBIoT小区:'))
    return df

def trans_AdditionalText(df,colname):
    pass

all_files = listdir(data_path)
files = [x for x in all_files if '.txt' in x ]
content_all = ''
for file in files:
    file_tmp = open(data_path + file)
    content = file_tmp.read()
    content_all = content_all + content

df_alarm = DataFrame()
df_alarm['网元'] = ''
df_alarm['告警名称'] = ''
df_alarm['告警单元'] = ''
df_alarm['告警级别'] = ''
df_alarm['告警处理优先级'] = ''
df_alarm['告警当前状态'] = ''
df_alarm['发生时间'] = ''
df_alarm['恢复时间'] = ''
df_alarm['故障原因'] = ''
df_alarm['附加信息'] = ''

alarm_name_dict ={ 'Heartbeat Failure':'基站掉站',
                    'Service Unavailable':'小区服务不可用',
                    'Resource Activation Timeout':'资源激活超时',
                    'Fan Failure':'风扇故障',
                    'No Connection':'连接丢失',
                    'Grace Period Activated':'自动扩容激活',
                    'Inconsistent Configuration':'配小区资源置不一致',
                    'RET Failure':'电调天线故障',
                    'RET Not Calibrated':'电调天线校准失败',
                    'Link Degraded':'BBU至RRU传输质量下降',
                    'Service Degraded':'小区服务质量下降',
                    'VSWR Over Threshold':'驻波比超限',
                    'HW Fault':'硬件故障',
                    'SW Fault':'软件故障',
                    'Link Failure':'BBU至RRU光纤故障',
                    'Power Loss':'RRU掉电',
                    'Resource Allocation Failure Service Degraded':'资源分配失败,服务质量下降',
                    'TimeSyncIO Reference Failed':'参考时钟故障',
                    'Calendar Clock Misaligned':'时钟校准失败',
                    'Synchronization End':'同步结束',
                    'Synchronization Start':'同步开始',
                    'PLMN Service Unavailable':'小区退出服务',
                    'SFP Stability Problem':'光模块故障',
                    'Calendar Clock NTP Server Unavailable':'NTP服务器不可用',
                    'Current Too High':'功率过载'}

alarm_priority_dict ={ 'Heartbeat Failure':'影响业务_需优先处理',
                    'Service Unavailable':'影响业务_需优先处理',
                    'Resource Activation Timeout':'不影响业务_无需处理',
                    'Fan Failure':'影响业务_需处理',
                    'No Connection':'影响业务_需处理',
                    'Grace Period Activated':'不影响业务_无需处理',
                    'Inconsistent Configuration':'影响业务_需处理',
                    'RET Failure':'影响业务_需处理',
                    'RET Not Calibrated':'不影响业务_无需处理',
                    'Link Degraded':'影响业务_需优先处理',
                    'Service Degraded':'不影响业务_无需处理',
                    'VSWR Over Threshold':'影响业务_需优先处理',
                    'HW Fault':'影响业务_需优先处理',
                    'SW Fault':'影响业务_需优先处理',
                    'Link Failure':'影响业务_需优先处理',
                    'Power Loss':'影响业务_需优先处理',
                    'Resource Allocation Failure Service Degraded':'不影响业务_无需处理',
                    'TimeSyncIO Reference Failed':'影响业务_需优先处理',
                    'Calendar Clock Misaligned':'不影响业务_无需处理',
                    'Synchronization End':'不影响业务_无需处理',
                    'Synchronization Start':'不影响业务_无需处理',
                    'PLMN Service Unavailable':'影响业务_需优先处理',
                    'SFP Stability Problem':'影响业务_需优先处理',
                    'Calendar Clock NTP Server Unavailable':'不影响业务_无需处理',
                    'Current Too High':'影响业务_需处理'}

alarm_class_dict ={ 'Critical':'紧急告警',
                    'Major':'主要告警',
                    'Minor':'次要告警',
                    'Warning':'警告告警',
                    'Indeterminate':'不确定告警',
                    'Cleared':'已恢复告警'}

alarm_cause_dict ={ 'LAN Error/Communication Error':'传输故障',
                    'x733UnderlyingResourceUnavailable':'x733基础资源不可用',
                    'gsm1211TimeoutExpired':'gsm1211超时',
                    'x733EquipmentMalfunction':'x733设备故障',
                    'x733ThresholdCrossed':'x733超过阈值',
                    'x733ConfigurationOrCustomizationError':'x733配置错误',
                    'gsm1211PowerSupplyFailure':'gsm1211供电故障',
                    'x733PerformanceDegraded':'x733性能下降',
                    'x733SoftwareError':'软件故障',
                    'm3100Unavailable':'m3100不可用'}


p1 = r'(AlarmId.*[\s\S]+?FDN2:)'  # 正则表达式，匹配一条完整的告警记录文件
alarm_list = re.findall(p1,content_all) # 通过正则匹配分割所有的告警记录
alarm_list = findall(p1,content_all) # 通过正则匹配分割所有的告警记录

i = 0
for j in range(0,len(alarm_list)):
    i += 1
    lines = alarm_list[j].split('\n')
    for line in lines:
        if 'ObjectOfReference:' in line:
            df_alarm.loc[i,'网元'] = line.split(',')[2].split('=')[1].strip()
        if 'SpecificProblem:' in line:
            df_alarm.loc[i,'告警名称'] = line.split(':')[1].replace('\n','').strip()
        if 'ObjectOfReference:' in line:
            df_alarm.loc[i,'告警单元'] = line.split(':')[1].split(',')[-3]\
                                        + ' '\
                                        + line.split(':')[1].split(',')[-2]\
                                        + ' '\
                                        + line.split(':')[1].split(',')[-1]
        if 'PerceivedSeverity:' in line:
            df_alarm.loc[i,'告警级别'] = line.split(':')[1].replace('\n','').strip()
        if 'EventTime:'in line:
            df_alarm.loc[i,'发生时间'] = line.split('EventTime:')[1].replace('\n','').strip()
        if 'CeaseTime:'in line:
            df_alarm.loc[i,'恢复时间'] = line.split('CeaseTime:')[1].replace('\n','').strip()
        if 'ProbableCause:'in line:
            df_alarm.loc[i,'故障原因'] = line.split(':')[1].replace('\n','').strip()
        if 'eriAlarmNObjAdditionalText:' in line:
            df_alarm.loc[i,'附加信息'] = line.split(':')[1].replace('\n','').strip()

df_alarm['告警处理优先级'] = df_alarm['告警名称'].map(alarm_priority_dict)
df_alarm['告警级别'] = df_alarm['告警级别'].map(alarm_class_dict)
df_alarm['告警名称'] = df_alarm['告警名称'].map(alarm_name_dict)
df_alarm['故障原因'] = df_alarm['故障原因'].map(alarm_cause_dict)

df_alarm = trans_AlarmUnit(df_alarm)


current_time = str(datetime.now()).split('.')[0].replace(':','.')

with pd.ExcelWriter(data_path + '爱立信存留告警' + current_time + '.xlsx' ) as writer:
     df_alarm.to_excel(writer,'爱立信存留告警',index = False)
