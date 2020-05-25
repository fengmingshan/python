# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 09:47:48 2017
已经封装过的最终版,测试成功
爬取猫眼电影网TOP100电影
@author: Administrator
"""

import requests            #导入requests库  
from bs4 import BeautifulSoup   #导入BeautifulSoup库  
from requests.exceptions import RequestException     #导入requests库中的错误和异常字段   
import json                      #导入json库  

def get_one_page(url):        #定义爬取一个页面的函数
    try:                      #尝试打开页面
        response = requests.get(url)
        if response.status_code==200:
            return response.text  #如果页面打开成功则返回所打开网页的内容
        return None                   #如果页面打开不成功则返回“None”
    except  RequestException :        #如果发生错误或异常则返回“None”
        return None

def prase_one_page(html):      #定义解析一个页面的程序
    soup=BeautifulSoup(html,'lxml')
    moivelist=['豆瓣电影TOP250']
    for item in soup.findAll("div",class_="item"):
        em=item.select('em')[0].text                                  #获取排名
        a=item.select('a')[0]['href']                                 #获取影片链接
        img=item.select('img')[0]['src']                              #获取影片图片
        title=item.select('.title')[0].text.replace('\xa0','')        #获取影片名称
        titleAll=title
        if len(item.select('.title'))>1:                             #获取影片别名          
            title1=item.select('.title')[1].text.replace('\xa0','')  #因为影片别名中有日文和韩文影响输出，所以不使用
            titleAll+=title1
        titleother=item.select('.other')[0].text.replace('\xa0','')  #获取影片其他名称
        titleAll+=titleother                                       #获取影片名称和其他名称
        actor =item.select('p')[0].text.replace(' ','')            #获取影片信息
        actorsplited=actor.split('\n')
        actors=actorsplited[1].replace('\xa0','')                  #获取影片导演演员信息
        otherinfos=actorsplited[2]                                 #获取影片其他信息
        otherinfosplited= otherinfos.replace('\xa0','').split('/') #分隔影片其他信息
        releasetime=otherinfosplited[0]                            #从分隔影片其他信息中获得发布时间
        releasecountry=otherinfosplited[1]                         #从分隔影片其他信息中获得国家
        typename=otherinfosplited[2]                               #获取影片类型
        score=item.select('.rating_num')[0].text                   #获取影片评分
        #quote=item.select('.quote')[0].text.replace('\n','')       #获取影片经典台词
        dic={"em":em,"a":a,"img":img,"title":titleAll,"actor":actors,"releasetime":releasetime,"releasecountry":releasecountry,"typename":typename,"score":score}
        moivelist.append(dic)
    return moivelist

def write_to_file(content):       #定义输出到文件的程序
    with open(r'D:\python\movielist.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
        f.write(json.dumps(content,ensure_ascii=False)+'\n')      #打开写入文件编码方式：utf-8    
        f.close()
        
def main():                #定义主程序
    for i in range (10):
        pagecount=i*25
        pagestr=__builtins__.str(pagecount)
        url="https://movie.douban.com/top250?start="+pagestr+"&filter="   #每25个电影翻一页
        html=get_one_page(url)                                            #调用爬取网页子程序
        moivelist=prase_one_page(html)                                    #解析解析网页子程序
        Filecontent = moivelist[1:]                                       #将moivelist赋值给写入文件内容Filecontent
        for Filecontent in  moivelist:                                    #从第一部电影开始逐行写入
            write_to_file(Filecontent)                                    #调用输出到文件子程序

if __name__=='__main__':        #python最终封装，python的固定格式
    main()
  