# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:38:06 2020

@author: Administrator
"""

import json
from urllib.request import urlopen, quote
import requests
def getlnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'hGWFzj6whiB3W2RFteYtaiiCKrPca8nM' # 百度地图ak，具体申请自行百度，提醒需要在“控制台”-“设置”-“启动服务”-“正逆地理编码”，启动
    address = quote(address) # 由于本文地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak +'&callback=showLocation%20'+'//GET%E8%AF%B7%E6%B1%82'
#   req = urlopen(uri)
#   res = req.read().decode() 这种方式也可以，和下面的效果一样，都是返回json格式
    res=requests.get(uri).text
    temp = json.loads(res) # 将字符串转化为json
    
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat,lng# 纬度 latitude,经度 longitude

address='罗平县阿岗镇新寨小学'
getlnglat(address)