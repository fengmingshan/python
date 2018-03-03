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
from io import BytesIO  
  



#File=os.listdir(r'D:\Packet')  #第一步取得文件夹里的所有文件名
file_path=r'D:\Packet'
file_name='20180131-3.txt'

file_content= open(file_path+'\\'+file_name,'r',encoding='utf-8') 
text=file_content.readlines()
text_tmp=text[-1].split('=',1)
text_tmp1=text_tmp[-1]
text_url_decode=parse.unquote(text_tmp1)    #对b进行url解码
text_json_decode=json.loads(text_url_decode)
file1=text_json_decode[0]['data']
file2=text_json_decode[1]['data']

file1=bytes(file1,encoding='utf-8')
file2=bytes(file2,encoding='utf-8')




file1_b64_decode = base64.b64decode(file1)
file2_b64_decode = base64.b64decode(file2)

file1_comp=file1_b64_decode[:-388]
file2_comp=file1_b64_decode[:-388]

def gzip_uncompress(c_data):  
    '''定义gzip解压函数'''
    buf =BytesIO(c_data)   # 通过IO模块的BytesIO函数将Bytes数据输入，这里也可以改成StringIO，根据你输入的数据决定
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  

file1_uncompress=gzip_uncompress(file1_comp)
file2_uncompress=gzip_uncompress(file2_comp)

print(file1_uncompress.decode('utf-8'))
print(file2_uncompress.decode('utf-8'))










