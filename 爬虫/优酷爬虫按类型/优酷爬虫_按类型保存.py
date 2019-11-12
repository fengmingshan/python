# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:01:05 2019

@author: 1
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#----------------------------------------------------------------
#爬区所有分类节目网址
#----------------------------------------------------------------
data=[]
url = 'http://list.youku.com/category/video'
try:
    response = requests.get(url)
    bs = BeautifulSoup(response.text, features='html5lib')
    items=bs.select("div[class='item noborder'] a") # CSS 选择器
    #    items = bs.select('.box-video .yk-col4')
        #print(items)
    i=0
    colum=['youku_name','youku_http']
    df=pd.DataFrame(index=None,columns=colum)
    for item in items:
        youku_name = item.get_text()  #节目
        youku_http1 =item.get('href') #网址
        youku_http2 ="http://list.youku.com"+youku_http1
        df.loc[i,'youku_name']=youku_name
        df.loc[i,'youku_http']=youku_http2
        i+=1
finally:
    response.close()

#-----------------------------------------------------------
#           爬区分类节目相应内容
#-----------------------------------------------------------
data1=[]
num_rows=df.iloc[:,0].size
for rown in range(0,num_rows):
    url =df.loc[rown,'youku_http']
    page=df.loc[rown,'youku_name']
    try:
        response = requests.get(url)
        bs = BeautifulSoup(response.text, features='html5lib')
        items=bs.select("li[class='title'] a") # CSS 选择器
   #    items = bs.select('.box-video .yk-col4')
        #print(items)
        for item in items:
            youku_name = item.get_text()  #风景区
            youku_http1 =item.get('href') #风景区
            data1.append({'youku_name':youku_name,'youku_http1':("http:"+youku_http1)})
            df1 = pd.DataFrame(data1) 
            df1=df1[['youku_name','youku_http1']]
            df1.to_csv('F:\\movie\\{}.txt'.format(page), sep='\t', index=False)
    finally:
            response.close()

