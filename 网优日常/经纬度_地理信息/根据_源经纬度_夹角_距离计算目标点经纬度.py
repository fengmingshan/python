import geopy.distance

def calc_direction_distance_point(lat, lon, distance, direction):
    """
    根据经纬度，距离，方向获得一个地点
    :param lat: 纬度
    :param lon: 经度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.GeodesicDistance(meters=distance)
    point = d.destination(point=start, bearing=direction)
    return (round(point.longitude,6),round(point.latitude,6) )

p = calc_direction_distance_point( 25.509586, 103.755795, 250, 60)
p
