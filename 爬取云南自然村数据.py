# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 19:53:49 2018
从云南数字乡村网爬取所有自然村的信息
@author: Administrator
"""
import requests            #导入requests库  
from bs4 import BeautifulSoup   #导入BeautifulSoup库  
from requests.exceptions import RequestException     #导入requests库中的错误和异常字段   
import json                      #导入json库  

url=r'http://ynszxc.gov.cn' 
url_city=r'http://ynszxc.gov.cn/S1/S176/'   #定义首页的地址

def write_to_file(content):       #定义输出到文件的程序
    with open(r'D:\test\qujing_village.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
        f.write(json.dumps(content,ensure_ascii=False)+'\n')      #打开写入文件编码方式：utf-8    
        f.close()


def get_one_page(url):        #定义爬取一个页面的函数
    try:                      #尝试打开页面
        response = requests.get(url)
        response.encoding='GB2312' #在网页上通过F12查看源代码得到编码方式是GB2312
        if response.status_code==200:
            return response.text  #如果页面打开成功则返回所打开网页的内容
        return None                   #如果页面打开不成功则返回“None”
    except  RequestException :        #如果发生错误或异常则返回“None”
        return None

html=get_one_page(url_city)
soup=BeautifulSoup(html,'lxml')
content=soup.findAll("option") #找出所有的下拉菜单
country_info={}
country_tmp=[]
for i in content:
    country_tmp.append(((i.string.strip()),i.attrs['value']))   
country_tmp=country_tmp[1:]
country_info=dict(country_tmp)

for i in country_info.values():
    url_county=url+i
    html=get_one_page(url_county)
    soup=BeautifulSoup(html,'lxml')
    content=soup.findAll('div',class_='rowthree')   #class=rowthree的div结构
    for item in content:
        town=item.findAll('a')
    town_info={}
    town_tmp=[]
    for j in town:
        town_tmp.append((j.string,j.attrs['href']))
    town_info=dict(town_tmp)      #形成村庄名称和链接的字典
    
    for j in list(town_info.keys()):
        if town_info[j] in ['#']:
            del town_info[j]     #删除村庄信息字典中，值为#的无用项目    
    
    for j in town_info.values(): #通过迭代依次打开乡镇，抓取村庄信息
        url_town=url+j
        html=get_one_page(url_town)
        soup=BeautifulSoup(html,'lxml')
        content=soup.findAll('div',class_='rowthree')   #class=rowthree的div结构  
        for item in content:
            village=item.findAll('a')
        village_info={}
        village_tmp=[]
        for k in village:
            village_tmp.append((k.string,k.attrs['href']))
        village_info=dict(village_tmp)     #形成村庄名称和链接的字典
        
        for k in list(village_info.keys()):
            if village_info[k] in ['#']:
                del village_info[k]     #删除村庄信息字典中，值为#的无用项目    
                
        for k in village_info.values(): #通过迭代依次打开乡镇，抓取村庄信息
            url_village=url+k
            html=get_one_page(url_village)
            soup=BeautifulSoup(html,'lxml')
            content=soup.findAll("option")   #class=rowthree的div结构  
            point_info={}
            point_tmp=[]
            for item in content:
                point_tmp.append((item.string,iteml.attrs['value']))
            point_info=dict(village_tmp)       #形成村庄名称和链接的字典
            
        
        
                
            
        



        
        
        



        
        
    



            
        
        
    
        

    


