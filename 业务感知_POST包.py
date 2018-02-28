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
c=json.dumps(b_url)
tmp=c.split('"}',2)
d=tmp[0].split(':\\"',3)
d_tmp=d[3].encode('utf-8')
enTest = base64.encodestring(d_tmp)
enTest=str(enTest,'utf-8')


def gzip_uncompress(c_data):  
    buf = StringIO(c_data)  
    f = gzip.GzipFile(mode='wb',fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  

data=gzip_uncompress(enTest)










