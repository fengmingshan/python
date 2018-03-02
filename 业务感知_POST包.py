# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:59:50 2018

@author: Administrator
"""
import os
import json
from urllib import parse
from urllib import request
import base64
import gzip
from io import StringIO
import zlib
import demjson

#File=os.listdir(r'D:\Packet')  #第一步取得文件夹里的所有文件名
D=r'D:\Packet'

f='20180131-3.txt'

F= open(D+'\\'+f,'r',encoding='utf-8') 
text=F.readlines()
a=text[-1].split('=',1)
b=a[-1]
b_url=parse.unquote(b)    #对b进行url解码
#c=json.dumps(b_url)
#tmp=c.split('"}',2)
#d=tmp[0].split(':\\"',3)
#d_tmp=d[3].encode('utf-8')
c=b_url.split('data":"',2)
d1=c[1].split('"},')
d2=c[2].split('"},')
file1=d1[0]

d3=d2[0].split('"}')
file2=d3[0]

file1_li=file1.split('\\n')

file1=bytes(file1,encoding='utf-8')
file2=bytes(file2,encoding='utf-8')

file1_en = base64.encodestring(file1)
file2_en = base64.encodestring(file2)
file1_str=file1_en
file1_en=bytes().fromhex(file1_en)

print(file1_en)
print(file2_en)


file1_unzip=gzip.decompress(file1_en)
file2_unzip=gzip.decompress(file2_en)












