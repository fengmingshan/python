# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 20:22:41 2018

@author: Administrator
"""
import requests            #导入requests库
from bs4 import BeautifulSoup   #导入BeautifulSoup库
from requests.exceptions import RequestException     #导入requests库中的错误和异常字段
import json                      #导入json库

url="https://movie.douban.com/top250"   #网址
# 伪装成浏览器,应付网站的反爬虫设置
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

response = requests.get(url,headers=headers)
res=response.text
soup=BeautifulSoup(res,'lxml')
moivelist=['豆瓣电影TOP250']

for item in soup.findAll("div",class_="item"):
    em=item.select('em')[0].text                                  #获取排名
    a=item.select('a')[0]['href']                                 #获取影片链接
    img=item.select('img')[0]['src']                              #获取影片图片
    title=item.select('.title')[0].text.replace('\xa0','')        #获取影片名称
    titleAll=title
    if len(item.select('.title'))>1:                         #获取影片别名
        title1=item.select('.title')[1].text.replace('\xa0','')  #因为影片别名中有日文和韩文影响输出，所以不使用
        titleAll+=title1
    titleother=item.select('.other')[0].text.replace('\xa0','')  #获取影片其他名称
    titleAll+=titleother                                       #获取影片名称和其他名称
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

with open(r'C:\Users\Administrator\Desktop\movielist.txt','w',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
    for content in  moivelist:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')      #打开写入文件编码方式：utf-8
    f.close()

