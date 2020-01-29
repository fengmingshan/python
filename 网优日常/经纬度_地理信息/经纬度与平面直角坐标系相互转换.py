# -*- coding: utf-8 -*-
"""
Created on Mon May 27 09:38:15 2019

@author: Administrator
"""

xy_coordinate = [] # x，y坐标集
def millerToXY (lon, lat):
     '''
     经纬度转换为平面坐标系中的x,y 利用米勒坐标系
     :param lon: 经度
     :param lat: 维度
     '''
     L = 6381372*math.pi*2
     W = L
     H = L/2
     mill = 2.3
     x = lon*math.pi/180
     y = lat*math.pi/180
     y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
     x = (W/2)+(W/(2*math.pi))*x
     y = (H/2)-(H/(2*mill))*y
     xy_coordinate.append((int(round(x)),int(round(y))))
     return xy_coordinate # 装换后的 x,y 坐标


lonlat_coordinate = []  # 经纬度坐标集
def millerToLonLat(x,y):
     """
     将平面坐标系中的x,y转换为经纬度，利用米勒坐标系
     :param x: x轴
     :param y: y轴
     :return:
     """
     L = 6381372 * math.pi*2
     W = L
     H = L/2
     mill = 2.3
     lat = ((H/2-y)*2*mill)/(1.25*H)
     lat = ((math.atan(math.exp(lat))-0.25*math.pi)*180)/(0.4*math.pi)
     lon = (x-W/2)*360/W
     # TODO 最终需要确认经纬度保留小数点后几位
     lonlat_coordinate.append((round(lon,5),round(lat,5)))
     return lonlat_coordinate
