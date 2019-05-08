# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:57:51 2019

@author: Administrator
"""

import os
import json
import requests
import base64
import gzip
from io import StringIO
from io import BytesIO  
# =============================================================================
# 第一个数据包
# =============================================================================
# 数据包header
headers = {
"Connection": "close",
"Charset": 'UTF-8',
"X-SECU":'9CF279BEE18C1689AD00000148047583',
"Content-Type": 'application/X-cfg-upg-cache',
"User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; MI MAX MIUI/V10.2.1.0.NBDCNXM)',
'Host': '42.99.18.27:9777',
"Accept-Encoding": "gzip",
"Content-Length": '0'
}
url = 'http://42.99.18.27:9777/cfg/0'
data =  {'ue-mac':'78:02:F8:66:3E:A6',
         'imei':'99000836929878',
         'ab-code':'68',
         'seq':''
}
# post数据包
response_content = requests.post(url = url,data = data, headers = headers).content;
print(response_content)

# 建立session方式获取
data =  {'ue-mac':'78:02:F8:66:3E:A6',
         'imei':'99000836929878',
         'ab-code':'68',
         'seq':''
}


# =============================================================================
# 第二个数据包
# =============================================================================
# 数据包header
headers = {
"Connection": "close",
"Charset": 'UTF-8',
"X-SECU":'9CF279BEE18C1689AD00000148047583',
"Content-Type": 'application/X-cfg-upg-cache;charset= "UTF-8"',
"User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; MI MAX MIUI/V10.2.1.0.NBDCNXM)',
'Host': '42.99.18.27:9777',
"Accept-Encoding": "gzip",
"Content-Length": '0'
}
url = 'http://42.99.18.27:9777/cfg/1'
data =  {'seq' : '0',
         'ab-code' : '68',
         'imei' : '99000836929878',
         'city' : 'e69bb2e99d96e5b882',
         'prov' : 'e4ba91e58d97e79c81',
         'area-code' : '249',
         'ue-mac' : '78:02:F8:66:3E:A6',
         'imsi' : '460110554863125',
         'vendor' : '5869616f6d69',
         'model' : '4d49204d4158'
}
# post数据包
response = requests.post(url = url,data = j_data, headers = headers);

print(response)

# =============================================================================
# 下载测试模板
# =============================================================================
# 数据包header
headers = {
"Connection": "close",
"Charset": 'UTF-8',
"X-SECU":'9CF279BEE18C1689AD00000148047583',
"Content-Type": 'application/X-cfg-upg-cache',
"User-Agent": 'Dalvik/2.1.0 (Linux; U; Android 7.0; MI MAX MIUI/V10.2.1.0.NBDCNXM)',
'Host': '42.99.18.27:9778',
"Accept-Encoding": "gzip",
"Content-Length": '0'
}
url = 'http://42.99.18.27:9778/fil'
data =  {'markid' : 'c839061bca1a434c98206bc400327c0b.xml.gzip',
         'imei' : '99000836929878',
         'ue-mac' : '78:02:F8:66:3E:A6'
}
# post数据包
response = requests.get(url = url,data = j_data, headers = headers);

print(response.text)


