import geopy.distance

def get_distance_point(lat, lon, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.VincentyDistance(meters=distance)
    return d.destination(point=start, bearing=direction)

p = get_distance_point( 25.509586, 103.755795, 250, 60)
print (round(p.longitude,6),round(p.latitude,6) )
