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
from selenium import webdriver 
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait #等待页面加载某些元素
import sys   
sys.setrecursionlimit(1000000)   #修改系统最大递归数量
                  
browser=webdriver.PhantomJS()
url=r'http://ynszxc.gov.cn' 
url_city=r'http://ynszxc.gov.cn/S1/S176/'   #定义首页的地址
F=open(r'D:\test\曲靖自然村信息_略.txt','r',encoding='utf-8')
text_tmp=F.readlines()   #读取地名文件中的所有行，读完之后返回一个list
text=[]                  #构造空list用于存储去换行符号后的新地名
for line in text_tmp:
    line=line.replace('\n','')   #替换自然村名最后的换行符号
    text.append(line)            #构造自然村名信息的list，用于进行断点续爬 



def write_to_file(content):       #定义输出到文件的程序
    with open(r'D:\test\曲靖自然村信息.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
        f.write(json.dumps(content,ensure_ascii=False)+'\n')     
        f.close()

def write_to_file2(content2):       #定义输出到文件的程序
    with open(r'D:\test\曲靖自然村信息_略.txt','a',encoding='utf-8') as f:  #打开写入文件编码方式utf-8
        f.write(content2+'\n')      
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

def get_town(url):
    html=get_one_page(url)
    soup=BeautifulSoup(html,'lxml')
    content=soup.findAll('div',class_='rowthree')   #class=rowthree的div结构
    for item in content:
        town=item.findAll('a')
    town_info={}
    town_name=[]
    town_url=[]
    town_tmp=[]
    for i in town:
        town_tmp.append((i.string,i.attrs['href']))
    town_info=dict(town_tmp)      #形成乡镇名称和链接的字典
    for j in list(town_info.keys()):
        if town_info[j] in ['#']:
            del town_info[j]     #删除村庄信息字典中，值为#的无用项目 
    return town_info

def get_point(url):
    point_info={}
    html=get_one_page(url)
    if html:
        soup=BeautifulSoup(html,'lxml')
        content=soup.find_all("option") #找出所有的下拉菜单
        point_name=[]
        point_url=[]
        url_tmp=[]
        point_tmp=[]
        for item in content:   
            point_name.append(item.text.strip()[3:])
            url_tmp.append(item.attrs)
        if point_name:
            del point_name[0] #删除下拉菜单中的前两项无用信息
            del url_tmp[0]
            url_tmp[0]['value']=url[20:]  #因为option下拉菜单中行政村本身的url为，所以单独对行政村的url进行赋值
            for i in range(0,len(url_tmp),1):
                point_url.append(url_tmp[i]['value'])
                point_tmp.append((point_name[i],point_url[i]))     
        point_info=dict(point_tmp)      #形成乡镇名称和链接的字典
    return point_info

def get_introduce(url):
    browser=webdriver.PhantomJS()
    point_introduce=''
    try:
        browser.get(url)
        browser.implicitly_wait(3)  
        #if browser.find_element_by_id('IframeText'):
        browser.switch_to_frame('IframeText')
        wait=WebDriverWait(browser,10)
        wait.until(EC.presence_of_element_located((By.ID,'text')))
        point=browser.find_element_by_id('text')
        point_introduce=point.text 
        browser.quit()
        return point_introduce 
    except Exception as e:
        browser.quit()
        with open(r'D:\test\曲靖自然村信息.txt','a',encoding='utf-8') as f_result:
        f_result.write(url+'\n')
        return None
    #finally:       
        #browser.quit()
        

html=get_one_page(url_city)
soup=BeautifulSoup(html,'lxml')
content=soup.findAll("option") #找出所有的下拉菜单
country_info={}
country_name=[]
country_url=[]
country_tmp=[]
for i in content:
    country_name.append(i.string.strip())
    country_url.append(i.attrs['value'])
del country_name[0]
del country_url[0]

for i in range(0,len(country_name),1):
    country_tmp.append((country_name[i],country_url[i]))
country_info=dict(country_tmp) #形成县城名称和链接的字典

for i in country_info.keys(): #通过迭代依次打开县城，抓取乡镇信息
    url_county=url+country_info[i]
    town_info= get_town(url_county)  
    
    for j in town_info.keys(): #通过迭代依次打开乡镇，抓取村庄信息
        url_town=url+town_info[j]
        village_info=get_town(url_town)     #因为行政村的页面格式与乡镇town一样，所以直接用get_town
                
        for k in village_info.keys(): #通过迭代依次打开行政村，抓取自然信息
            url_village=url+village_info[k]
            point_info=get_point(url_village)
            
            for l in point_info.keys():
                string= i+'_'+j+'_'+k+'_'+l     #构造当前爬取的自然村名
                if string not in  text:     #断点判断，当前的自然村是否已经爬过了
                    url_point=url+point_info[l]
                    point_introduce=get_introduce(url_point)
                    dic={"city":'曲靖',"country":i,"town":j,"village":k,"point":l,"introduce":point_introduce}
                    str_point=i+'_'+j+'_'+k+'_'+l
                    write_to_file(dic)  
                    write_to_file2(str_point)
                    

                
            