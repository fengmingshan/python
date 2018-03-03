# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 09:03:49 2017

@author: Administrator
"""

import requests
response = requests.get("http://www.baidu.com")

print(response.text)
print(response.encoding)

response.encoding='utf-8'
print(response.txt)


soup=BeautifulSoup(response.text,'lxml')
print(soup.title.text)
print(soup.prettify())
print(soup.body.text)

print(soup.findAll.("a")):
for x in soup.findAll.("a"):
    print(x)
    
    
selecet ('p')   #selecet Tag直接加名字
selecet ('a') 
selecet ('img') 
selecet ('em')
selecet ('text')  
selecet ('css')  


selecet ('.title')   #selecet 样式表
selecet ('.other') 


 selecet ('#content') #selecet id名称
 


