# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 22:49:32 2018

@author: Administrator
"""
import base64
import gzip
from io import StringIO

# gzip read a compress file 
with gzip.open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt.gz', 'rb') as f:
    file_content = f.read()
    print(file_content)

# create a compressed GZIP file: 
content = b"Lots of content here"
with gzip.open('/home/joe/file.txt.gz', 'wb') as f:
    f.write(content)

# GZIP compress an existing file:
import shutil
with open(file, 'rb') as f_in:
    with gzip.open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)



# Base64编解码测试：
str1 = 'This is Test String'
str1=str1.encode('utf-8')
enTest = base64.encodestring(str1)
print('编码后：',enTest)
#对字符串进行解码
deTest = base64.decodestring(enTest)
print('解码后：',deTest)

# gzip压缩解压缩测试
def gzip_compress(raw_data):  
    buf = StringIO()  
    f = gzip.GzipFile(mode='wb', fileobj=buf)  
    try:  
        f.write(raw_data)  
    finally:  
        f.close()  
    return buf.getvalue()  

def gzip_uncompress(c_data):  
    buf = StringIO(c_data)  
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  

str2=b'This is Test String'

zip_data = gzip.compress(str2)
print('压缩后：',zip_data)

unzip_data=gzip.decompress(zip_data)
print('解压缩：',unzip_data)

# 压缩string
fp = open(r'D:\2018年工作\2018年3月感知系统编程\file2.txt') 
lines=fp.readlines
s_in = b"Lots of content here"
s_out = gzip.compress(s_in)







