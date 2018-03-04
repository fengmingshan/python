# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 20:22:41 2018

@author: Administrator
"""
import requests            #导入requests库  
from requests.exceptions import RequestException     #导入requests库中的错误和异常字段   
import re
import json                      #导入json库  

url=r"https://movie.douban.com/top250"   #网址
response = requests.get(url)
content=response.text
moivelist=['豆瓣电影TOP250']
# 爬影片排名
p_em=r'<em class="">\d+?</em>' # 写正则表达式 
pattern_em = re.compile(p_em) # 编译正则表达式
em = re.findall(pattern_em,content) # 搜索整个网页内容

# 爬影片链接
p_a=r'<a href="https://movie.douban.com/subject/.+/">'
pattern_a = re.compile(p_a) # 编译正则表达式
a = re.findall(pattern_a,content) # 搜索整个网页内容

# 爬影片图片
p_img=r'<img width=.+class="">'
pattern_img = re.compile(p_img) # 编译正则表达式
img = re.findall(pattern_img,content) # 搜索整个网页内容

# 爬取影片名称 和 别名，因为有的影片没有别名后期数据缺失不好处理，所以两个名字一起爬
p_title=r'<span class="title">[\u4e00-\u9fa5]+</span>[\s\S]{1}s.+'
pattern_title = re.compile(p_title) # 编译正则表达式
title = re.findall(pattern_title,content) # 搜索整个网页内容

# 爬取影片其他名称 
p_titleother=r'<span class="other">.+</span>'
pattern_titleother = re.compile(p_titleother) # 编译正则表达式
titleother = re.findall(pattern_titleother,content) # 搜索整个网页内容

actor =item.select('p')[0].text.replace(' ','')            #获取演员信息
actorsplited=actor.split('\n')
actors=actorsplited[1].replace('\xa0','')                  #获取影片导演演员信息
otherinfos=actorsplited[2]                                 #获取影片其他信息
otherinfosplited= otherinfos.replace('\xa0','').split('/') #分隔影片其他信息
releasetime=otherinfosplited[0]                            #从分隔影片其他信息中获得发布时间
releasecountry=otherinfosplited[1]                         #从分隔影片其他信息中获得国家
typename=otherinfosplited[2]                               #获取影片类型
score=item.select('.rating_num')[0].text                   #获取影片评分
quote=item.select('.quote')[0].text.replace('\n','')       #获取影片经典台词
dic={"em":em,"a":a,"img":img,"title":titleAll,"actor":actors,"releasetime":releasetime,"releasecountry":releasecountry,"typename":typename,"score":score,"quote":quote}
moivelist.append(dic)
    
with open(r'D:\python\movielist.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
    for content in  moivelist:   
        f.write(json.dumps(content,ensure_ascii=False)+'\n')      #打开写入文件编码方式：utf-8    
    f.close()

