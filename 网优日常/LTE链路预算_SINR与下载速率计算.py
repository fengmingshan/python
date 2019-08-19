# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 10:54:25 2019

@author: Administrator
"""
from math import log
from numpy import square

# =============================================================================
# LTE 下行链路预算
# ======= ======================================================================

def calc_a_Hm(area_type,Hm,f):
    if area_type == '密集市区':
        α_Hm  = 3.2*square((log(11.75*Hm,10))) - 4.97
    elif area_type == '城区':
        α_Hm  = (1.1*log(f,10)-0.7)*Hm-(1.56*log(f,10)-0.8)
    elif area_type == '农村':
        α_Hm  = (1.1*log(f,10)-0.7)*Hm-(1.56*log(f,10)-0.8)
    return round(α_Hm,4)

def calc_B_LNF(area_type , location):
    if area_type == '农村' and location == '室外':
        B_LNF = 6
    elif area_type == '城区'and location == '室外':
        B_LNF = 8
    elif area_type == '密集城区'and location == '室外':
        B_LNF = 10
    elif area_type == '农村'and location == '室内':
        B_LNF = 10
    elif area_type == '城区'and location == '室内':
        B_LNF = 12
    elif area_type == '密集城区'and location == '室内':
        B_LNF = 14
    return B_LNF

def calc_L_path(area_type ,f, Hb,Distance,α_Hm):
    if area_type == '城市' :
        L_path = 69.55 + 26.16*log(f,10) - 13.82*log(Hb,10) - α_Hm + (44.9 - 6.55*log(Hb,10))*log(Distance,10)
    elif area_type == '农村' :
        L_path = 69.55 + 26.16*log(f,10) - 13.82*log(Hb,10) - α_Hm + (44.9 - 6.55*log(Hb,10))*log(Distance,10) - 2*square(log(f/28))-5.4
    return L_path
# 区域类型
area_type = '农村'

# 室内外
location = '室内'

# 路径损耗参数 f -频率（单位：Mhz),Hb-基站高度（单位：米），Distance-距离（单位：km），Hm-移动台高度 = 1.5（单位：米）
f = 800
Hb = 30
Distance = 1
Hm = 1.5
Gain_antenna =18

# 计算 α(Hm)

α_Hm = calc_a_Hm(area_type,Hm,f)

# 路径损耗计算
L_path = calc_L_path(area_type ,f, Hb,Distance,α_Hm)



# 天线增益 Gain_antenna 单位dB,LTE网络采用的天线一般都是18 dBi
Gain_antenna = 18

# 小区发射功率（W）
P_cell = 60

# 下行RB数量 N_RB，L800M时等于25，L1800M时75。
N_RB = 25


# 衰落余量 B_LNF
B_LNF = calc_B_LNF(area_type,location)

# 建筑物穿透损耗 L_BPL
L_BPL = 18

# 其中 Nt：每个个资源块（RB）上的热噪声
Nt = -121.4
# 其中 Nf：UE噪声余量
Nf = 7
# 其中 Nf：UE噪声余量
B_IDL = 3

# SINR计算公式
SINR = (10*log((P_cell*1000/N_RB),10) + Gain_antenna - L_path - B_LNF - L_BPL )-(Nt + Nf + B_IDL)
