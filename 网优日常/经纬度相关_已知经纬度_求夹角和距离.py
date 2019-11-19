# -*- coding: utf-8 -*-
"""
Created on Thu May 23 11:34:27 2019

@author: Administrator
"""
import math
from math import sin
from math import cos
from math import degrees
from math import radians
from math import atan2

# =============================================================================
# 计算夹角
# =============================================================================
def getDegree(latA, lonA, latB, lonB):
    """
    Args:
        point p1(latA, lonA)
        point p2(latB, lonB)
    Returns:
        bearing between the two GPS points,
        default: the basis of heading direction is north
    """
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)
    dLon = radLonB - radLonA
    y = sin(dLon) * cos(radLatB)
    x = cos(radLatA) * sin(radLatB) - sin(radLatA) * cos(radLatB) * cos(dLon)
    brng = degrees(atan2(y, x))
    brng = (brng + 360) % 360
    return brng

def calc_azimuth(lat1, lon1, lat2, lon2):
    lat1_rad = lat1 * math.pi / 180
    lon1_rad = lon1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    lon2_rad = lon2 * math.pi / 180

    y = math.sin(lon2_rad - lon1_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad)

    brng = math.atan2(y, x) * 180 / math.pi

    return float((brng + 360.0) % 360.0)

# =============================================================================
# 计算距离
# =============================================================================
def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(latA)
    radLonA = radians(lonA)
    radLatB = radians(latB)
    radLonB = radians(lonB)

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance

def calc_greate_circle_distance(lat1, lon1, lat2, lon2):
    R = 6371393
    lat1_rad = lat1 * math.pi / 180
    lon1_rad = lon1 * math.pi / 180
    lat2_rad = lat2 * math.pi / 180
    lon2_rad = lon2 * math.pi / 180
    d = math.sqrt(math.pow(math.cos((lat1_rad + lat2_rad) / 2) * R * (lon1_rad - lon2_rad), 2) +
                  math.pow(R * (lat1_rad - lat2_rad), 2))
    if d < 10000:
        return float(d)
    else:
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return float(R * c)




