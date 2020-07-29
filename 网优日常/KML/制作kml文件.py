# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 14:12:44 2020

@author: Administrator
"""

from functools import reduce


style_yellow_pin = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
	<name>KmlFile</name>
	<Style id="s_ylw-pushpin_hl">
		<IconStyle>
			<scale>1.3</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
	<StyleMap id="m_ylw-pushpin">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_ylw-pushpin</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_ylw-pushpin_hl</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="s_ylw-pushpin">
		<IconStyle>
			<scale>1.1</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
			</Icon>
			<hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
		</IconStyle>
	</Style>
    {placemark}
</Document>
</kml>
'''

point_info = '''
    <Placemark>
		<name>{name}</name>
		<LookAt>
			<longitude>{lon}</longitude>
			<latitude>{lat}</latitude>
			<altitude>0</altitude>
			<heading>21.71258062711778</heading>
			<tilt>42.64566602657631</tilt>
			<range>1039.154137177595</range>
			<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
		</LookAt>
		<styleUrl>#m_ylw-pushpin</styleUrl>
		<Point>
			<gx:drawOrder>1</gx:drawOrder>
			<coordinates>{lon},{lat},0</coordinates>
		</Point>
	</Placemark>
'''

name_list = ['测试站1','测试站2','测试站3','测试站4']
lon_list = [103.3363, 103.3364, 103.3365, 103.3366]
lat_list = [25.9121, 25.9122, 25.9123, 25.9124]

place_list = []
for name,lon,lat in zip(name_list, lon_list, lat_list):
    text = point_info.format(name = name, lon = lon, lat = lat)
    place_list.append(text)
place = reduce(lambda x, y: x+y,place_list)

with open("D:/KML.kml", "w", encoding = 'utf-8') as f:
    f.writelines(style_yellow_pin.format(placemark = place))
