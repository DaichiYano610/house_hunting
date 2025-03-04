import math

def calc_distance(lat1: float,lon1: float,lat2: float,lon2: float)-> float:
    R = 6371
    distance = R * math.acos(
        math.sin(math.radians(lat1))*
        math.sin(math.radians(lat2))+
        math.cos(math.radians(lat1))*
        math.cos(math.radians(lat2))*
        math.cos(math.radians(lon1)-math.radians(lon2)))
    return distance