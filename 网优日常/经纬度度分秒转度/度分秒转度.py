# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:47:35 2020

@author: Administrator
"""

import re

lon1 = '103°56\'23"'
lat1 = '25°40\'48"'
lon2 = '103°52\'40"'
lat2 = '25°27\'29"'
lon3 = '103°52\'54"'
lat3 = '25°27\'20"'

x = re.match('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lon1)
x.group(1)
x.group(2)
x.group(3)

lo1 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lon1)
la1 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lat1)
lo2 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lon2)
la2 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lat2)
lo3 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lon3)
la3 = re.sub('(\d{1,3})°(\d{1,3})\'(\d{1,3})"', lambda x: str(float(x.group(1)) + float(x.group(2))/60 + float(x.group(3))/3660), lat3)

with open(r'C:\Users\Administrator\Desktop\lonlat.txt','w') as f :
    f.writelines('恩洪'+' '+lo1 +' '+ la1 + '\n')
    f.writelines('沿江'+' '+lo2 +' '+ la2 + '\n')
    f.writelines('石喇大寺'+' '+lo3 +' '+ la3 + '\n')