# -*- coding: utf-8 -*-
"""
Created on Wed May  6 23:43:34 2020

@author: Administrator
"""

import requests

params={"content":'''
①投诉原因：因有信号无法正常使用引发用户的投诉
②核实情况：根据用户诉求查询AN-AAA正常、AAA正常，HLR状态正常
③处理结果：投诉原因：市电停电，富宁里达共移动基站目前已经恢复正常，联系用户，用户不在投诉区域，建议用户返还投诉区域后使用观察，用户表示认可
④回复用户情况：（录音流水号 1901050000212832 ）12947回复用户认可、无异议
⑤说明备注：无； <br><br><br><b>回访信息</b><br><b>总体情况</b>：满意；  <b>处理态度</b>：满意；   <b>处理及时性</b>：满意； <b>处理结果</b>：满意；  <br><br><b>结果说明</b><br><b>问题产生原因</b>：；   <br><br><b>采取措施</b>：；  <br><br><b>原因分类</b>：移动业务->移动语音网络->无线网络原因->基站故障->基站设备故障；<br><br><b>处理结果</b>：<br><b>责任定性</b>：企业原因；<br><br><b>考核原因</b>：；<br><br><b>责任部门</b>：文山分公司【876】；<br><br><b>CRM流水号(操作)</b>：99999999999999；<br><br><b>备注</b>：
''',"clas":23}
r = requests.get("http://127.0.0.1:8000/classify", params=params)

print(r.json())
