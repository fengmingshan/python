# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:59:51 2020

@author: Administrator
"""


import pandas as pd
import os
from selenium import webdriver


path = r'D:\_python小程序\绘制小区RSRP覆盖热力图'
os.chdir(path)

SCELL = 186829875
HOUR = 21
df = pd.read_csv('栅格化数据_麒麟区.csv', engine='python')
df_cellinfo = pd.read_excel('cell_info.xlsx')
df_cellinfo = df_cellinfo[df_cellinfo['ECI'] == SCELL]

cell_lon = df_cellinfo.iloc[0,2]
cell_lat = df_cellinfo.iloc[0,3]
cell_direction = df_cellinfo.iloc[0,4]
cell_name = df_cellinfo.iloc[0,1]

df['lon'] = df['GRIDX']*0.00045
df['lat'] = df['GRIDY']*0.00045
df['rsrp'] = df['AVG_SCRSRP']*-1

df.columns
#df['smaples'] = df['RSRP_SAMPLES']
df_scell = df[(df['SC_ECI'] == SCELL) & (df['NUM_HOURS'] == HOUR)]
df_scell = df_scell[['lon', 'lat', 'rsrp']]

# with open(r'C:\Users\Administrator\Desktop\hotmap.txt', 'w') as f:
#    f.writelines('    var points =['+'\n')
#    for i in range(len(df)):
#        f.writelines('{{"lng":{lon},"lat":{lat},"count":{num}}},'.format(
#            lon=df.loc[i, 'lon'], lat=df.loc[i, 'lat'], num=df.loc[i, 'avg_rsrp']))
#        f.writelines('\n')
#    f.writelines('];')

point_info = '    var points =['+'\n' + '\n'.join(['{{"lng":{lon},"lat":{lat},"count":{num}}},'.format(
    lon=lon, lat=lat, num=num) for lon, lat, num in zip(df_scell['lon'], df_scell['lat'], df_scell['rsrp'])]) + '];'


html = '''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=mq8kwN2R8UPBHqFEqP9pLnQTYVpy6N9G"></script>
    <script type="text/javascript" src="http://api.map.baidu.com/library/Heatmap/2.0/src/Heatmap_min.js"></script>
    <title>{cell_name}小区{hour}点RSRP覆盖图</title>
    <style type="text/css">
		ul,li{{list-style: none;margin:0;padding:0;float:left;}}
		html{{height:100%}}
		body{{height:100%;margin:0px;padding:0px;font-family:"微软雅黑";}}
		#container{{height:500px;width:100%;}}
		#r-result{{width:100%;}}
    </style>
</head>
<body>
	<div id="container"></div>
	<div id="r-result">
		<input type="button"  onclick="openHeatmap();" value="显示热力图"/><input type="button"  onclick="closeHeatmap();" value="关闭热力图"/>
	</div>
</body>
</html>
<script type="text/javascript">
    var map = new BMap.Map("container");          // 创建地图实例

  	var point = new BMap.Point({cell_lon}, {cell_lat});
    map.centerAndZoom(point, 15);             // 初始化地图，设置中心点坐标和地图级别
    map.enableScrollWheelZoom(); // 允许滚轮缩放

    {point_info}

    if(!isSupportCanvas()){{
    	alert('热力图目前只支持有canvas支持的浏览器,您所使用的浏览器不能使用热力图功能~')
    }}
	//详细的参数,可以查看heatmap.js的文档 https://github.com/pa7/heatmap.js/blob/master/README.md
	//参数说明如下:
	/* visible 热力图是否显示,默认为true
     * opacity 热力的透明度,1-100
     * radius 势力图的每个点的半径大小
     * gradient  {{JSON}} 热力图的渐变区间 . gradient如下所示
     *	{{
			.2:'rgb(0, 255, 255)',
			.5:'rgb(0, 110, 255)',
			.8:'rgb(100, 0, 255)'
		}}
		其中 key 表示插值的位置, 0~1.
		    value 为颜色值.
     */
	heatmapOverlay = new BMapLib.HeatmapOverlay({{"radius":50}});
	map.addOverlay(heatmapOverlay);
	heatmapOverlay.setDataSet({{data:points,max:140}});

    var vectorFCArrow = new BMap.Marker(new BMap.Point({cell_lon},{cell_lat}), {{
      // 初始化方向向上的闭合箭头
      icon: new BMap.Symbol(BMap_Symbol_SHAPE_FORWARD_CLOSED_ARROW, {{
        scale: 2,
        strokeWeight: 1,
        rotation: {cell_direction},//顺时针旋转30度
        fillColor: 'red',
        fillOpacity: 0.8
      }})
    }});
    map.addOverlay(vectorFCArrow);

	//是否显示热力图
    function openHeatmap(){{
        heatmapOverlay.show();
        vectorFCArrow.show();
    }}
	function closeHeatmap(){{
        heatmapOverlay.hide();
        vectorFCArrow.hide();
    }}
	closeHeatmap();
    function setGradient(){{
     	/*格式如下所示:
		{{
	  		0:'rgb(102, 255, 0)',
	 	 	.5:'rgb(255, 170, 0)',
		  	1:'rgb(255, 0, 0)'
		}}*/
     	var gradient = {{}};
     	var colors = document.querySelectorAll("input[type='color']");
     	colors = [].slice.call(colors,0);
     	colors.forEach(function(ele){{
			gradient[ele.getAttribute("data-key")] = ele.value;
     	}});
        heatmapOverlay.setOptions({{"gradient":gradient}});
    }}
	//判断浏览区是否支持canvas
    function isSupportCanvas(){{
        var elem = document.createElement('canvas');
        return !!(elem.getContext && elem.getContext('2d'));
    }}
</script>
'''

with open('d:/hotmap.html', 'w', encoding='utf-8') as f:
    f.writelines(html.format(point_info=point_info, cell_lon=cell_lon,
                             cell_lat=cell_lat, cell_direction=cell_direction,cell_name=cell_name,hour = HOUR))

driver = webdriver.Chrome()
driver.get("d:/hotmap.html")
