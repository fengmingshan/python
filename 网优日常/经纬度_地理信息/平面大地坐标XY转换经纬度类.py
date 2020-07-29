# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 17:37:02 2020

@author: Administrator
"""

import math

'''####################################################
类XYexchangeBL   进行WGS84坐标系下 的XY转为BL
                 X已东偏500000
                 需要手动输入中央经线 例如114.152的中央经线是111
####################################################'''
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率
class XYexchangeBL:
    '''###################
    #函数:get_WGS84_af(self)
    #WGS84椭球参数获得
    #返回长半轴a 扁率f
    ###################'''
    def get_WGS84_af(self):
        '''
         * WGS84
         * 长半轴a=6378137± 2（m）
         * 短半轴b=6356752.3142m
         * 扁率α=1/298.257223563
         * 第一偏心率平方 =0.00669437999013
         * 第二偏心率平方 =0.00673949674223
        '''
        a=6378137.0
        f=1/298.257223563
        return a,f

    '''###################
    #函数:Process_Degree(self,dD)
    #输入值 十进制的经纬度(DEG)
    #输出 度分秒的经纬度(DMS)
    ###################'''
    def Process_Degree(self,dD):
    	iDegree=int(dD)
    	dTmp=(dD-iDegree)*60
    	iMin=int(dTmp)
    	dSec=(dTmp-iMin)*60
    	dDegree=iDegree+float(iMin)/100+dSec/10000
    	return dDegree

    '''###################
    函数:XY2LatLon(self,ellipsoid,X, Y, L0)
    #输入值 ellipsoid指明椭球体: WGS84的参数是 84
    #      X、Y:  大地坐标X Y
    #      L0:中央经线 如：111
    #输出 度分秒的经纬度(DMS)
    ###################'''
    def XY2LatLon(self,ellipsoid,X, Y, L0):
        X=X/0.9996#仅针对UTM投影
        Y=Y/0.9996#针对UTM投影
        #椭圆参数控制
        if(ellipsoid==84):
            a,f=self.get_WGS84_af()

        iPI=0.0174532925199433333333#圆周率/180
        ProjNo=int(X/1000000)
        L0=L0*iPI


        X0=ProjNo*1000000+500000#东偏500000为后续步骤减去做铺垫
        Y0=0
        xval=X-X0
        yval=Y-Y0

        #e2=2*f-f*f#第一偏心率平方
        #e1=(1.0-math.sqrt(1-e2))/(1.0+math.sqrt(1-e2))
        #ee=e2/(1-e2)#第二偏心率平方
        e2=0.00669437999013
        e1=(1.0-math.sqrt(1-e2))/(1.0+math.sqrt(1-e2))
        ee=0.00673949674223


        M=yval
        u=M/(a*(1-e2/4-3*e2*e2/64-5*e2*e2*e2/256))

        #"\"表示转公式下一行结合在一起
        fai=u+(3*e1/2-27*e1*e1*e1/32)*math.sin(2*u)+(21*e1*e1/16-55*e1*e1*e1*e1/32)*math.sin(4*u)+(151*e1*e1*e1/96)*math.sin(6*u)+(1097*e1*e1*e1*e1/512)*math.sin(8*u)
        C=ee*math.cos(fai)*math.cos(fai)
        T=math.tan(fai)*math.tan(fai)
        NN=a/math.sqrt(1.0-e2*math.sin(fai)*math.sin(fai))
        R=a*(1-e2)/math.sqrt((1-e2*math.sin(fai)*math.sin(fai))*(1-e2*math.sin(fai)*math.sin(fai))*(1-e2*math.sin(fai)*math.sin(fai)))
        D=xval/NN
        #计算经纬度（弧度单位的经纬度）
        longitude1=L0+(D-(1+2*T+C)*D*D*D/6+(5-2*C+28*T-3*C*C+8*ee+24*T*T)*D*D*D*D*D/120)/math.cos(fai)
        latitude1=fai-(NN*math.tan(fai)/R)*(D*D/2-(5+3*T+10*C-4*C*C-9*ee)*D*D*D*D/24+(61+90*T+298*C+45*T*T-256*ee-3*C*C)*D*D*D*D*D*D/720)

        #换换为deg
        #longitude=self.Process_Degree(longitude1/iPI)
        #latitude=self.Process_Degree(latitude1/iPI)

        longitude=longitude1/iPI
        latitude=latitude1/iPI
        #return latitude,longitude
        return self.wgs84togcj02(latitude,longitude)

    '''###################
    函数:wgs84togcj02(self,lat,lng)
    #输入值 经纬度(DMS)
    #      lng : 经度
    #      lat : 纬度 如：111
    #输出 火星坐标(DMS)
    ###################'''
    def wgs84togcj02(self,lat,lng):
        """
        WGS84转GCJ02(火星坐标系)
        :param lng:WGS84坐标系的经度
        :param lat:WGS84坐标系的纬度
        :return:
        """
        # if out_of_china(self,lng, lat):  # 判断是否在国内
        #    return lng, lat
        dlat = self.transformlat(lng - 105.0, lat - 35.0)
        dlng = self.transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * pi
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [mglat,mglng]


    def transformlat(self,lng, lat):
        '''###################
        函数:transformlat(self,lng, lat)
        #输入值 经纬度(DMS)
        #输出 dlat
        ###################'''
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
            0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * pi) + 40.0 *
                math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
                math.sin(lat * pi / 30.0)) * 2.0 / 3.0
        return ret



    def transformlng(self,lng, lat):
        '''###################
        函数:transformlng(self,lng, lat)
        #输入值 经纬度(DMS)
        #输出 dlng
        ###################'''
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
            0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
                math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * pi) + 40.0 *
                math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
                math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
        return ret

'''
#运行示例
temp=XYexchangeBL()

Geo: 28°18'6.69"N,112°56'13.81"E 28.301858333333332,112.93716944444445
Map: 689953.9843,3132164.3037

Geo: 28°10'37.22"N,113°4'18.08"E 28.177005555555557,113.07168888888889
Map: 703384.6243,3118547.1158

Geo: 28°16'45.56"N,113°9'13.04"E 28.279294444444446,113.15362222222222
Map: 711228.7756,3130026.1752

Geo: 28°10'45.66"N,112°57'5.34"E 28.17935,112.95148333333333
Map: 691576.7008,3118611.2265
'''

b,l=temp.XY2LatLon(84,692417.6880,3123815.0629,111)
print(b,l)
print(b-28.133423,l-112.573925)
b,l=temp.XY2LatLon(84,742218.7207,2973934.4385,111)
print(b,l)
print(b-26.515796,l-113.261690)
b,l=temp.XY2LatLon(84,711228.7756,3130026.1752,111)
print(b,l)
print(b-28.279294444444446,l-113.15362222222222)
b,l=temp.XY2LatLon(84,691576.7008,3118611.2265,111)
print(b,l)
print(b-28.17935,l-112.95148333333333)

b,l=temp.XY2LatLon(84,457136.664,2455475.927,114)
print(b,l)
