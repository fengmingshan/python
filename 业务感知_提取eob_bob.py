# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 18:59:50 2018

@author: Administrator
"""
import os
import json
import base64
import gzip
import urllib
from urllib import parse
from io import BytesIO  

file_list = os.listdir(r'D:\Packet')  #第一步取得文件夹里的所有文件名
file_path = r'D:\Packet'+'\\'
out_path = r'D:\eob_bob'+'\\'

def gzip_uncompress(c_data):  
    '''定义gzip解压函数'''
    buf =BytesIO(c_data)   # 通过IO模块的BytesIO函数将Bytes数据输入，这里也可以改成StringIO，根据你输入的数据决定
    f = gzip.GzipFile(mode = 'rb', fileobj = buf)  
    try:  
        r_data = f.read()  
    finally:  
        f.close()  
    return r_data  

def get_eob_bob(file): 
    file_content= open(file_path+'\\'+file_name,'r',encoding='utf-8') 
    text=file_content.readlines()
    text_tmp=text[-1].split('=',1)
    text_tmp1=text_tmp[-1]
    text_url_decode=parse.unquote(text_tmp1)    #对b进行url解码
    text_json_decode=json.loads(text_url_decode)
    
    eob=text_json_decode[0]['data']
    bob=text_json_decode[1]['data']
    
    eob=bytes(eob,encoding='utf-8')
    bob=bytes(bob,encoding='utf-8')
    
    eob_b64_decode = base64.b64decode(eob)
    bob_b64_decode = base64.b64decode(bob)
    
    eob_comp=eob_b64_decode[:-388]
    bob_comp=eob_b64_decode[:-388]
    
    eob_uncompress=gzip_uncompress(eob_comp)
    bob_uncompress=gzip_uncompress(bob_comp)
    return (eob_uncompress,bob_uncompress)

def write_to_file(content,file_out):       #定义输出到文件的程序
    with open(file_out,'a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8，'a'表示追加写入
        f.write(content+'\n')      #打开写入文件编码方式：utf-8    
        f.close()

for file_name in file_list:
    file=file_path  + file_name
    eob_file_out=out_path + file_name[:-4]+'_eob.txt'
    bob_file_out=out_path + file_name[:-4]+'_bob.txt'
    content=get_eob_bob(file)
    write_to_file(content[0].decode('utf-8'),eob_file_out)
    write_to_file(content[1].decode('utf-8'),eob_file_out)
    
    








