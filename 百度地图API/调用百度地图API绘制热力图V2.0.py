# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 22:59:51 2020

@author: Administrator
"""


import pandas as pd


df = pd.read_excel(r'C:\Users\Administrator\Desktop\hotmap.xlsx')
df.columns
with open(r'C:\Users\Administrator\Desktop\hotmap.txt', 'w') as f:
    f.writelines('    var points =['+'\n')
    for i in range(len(df)):
        f.writelines('{{"lng":{lon},"lat":{lat},"count":{num}}},'.format(lon=df.loc[i,'LONB'], lat=df.loc[i,'LATB'], num=df.loc[i,'PCI']))
        f.writelines('\n')
    f.writelines('];')


html='''
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=mq8kwN2R8UPBHqFEqP9pLnQTYVpy6N9G"></script>
    <script type="text/javascript" src="http://api.map.baidu.com/library/Heatmap/2.0/src/Heatmap_min.js"></script>
    <title>热力图功能示例</title>
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

  	var point = new BMap.Point(103.798763, 25.503143);
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
	heatmapOverlay = new BMapLib.HeatmapOverlay({{"radius":20}});
	map.addOverlay(heatmapOverlay);
	heatmapOverlay.setDataSet({{data:points,max:504}});
	//是否显示热力图
    function openHeatmap(){{
        heatmapOverlay.show();
    }}
	function closeHeatmap(){{
        heatmapOverlay.hide();
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
with open(r'C:\Users\Administrator\Desktop\hotmap.txt', 'r') as f:
    point_info = f.read()

with open('d:/hotmap.html','w',encoding = 'utf-8') as f:
    f.writelines(html.format(point_info = point_info))
