"""
Created by Hrishikesh Ugale
10/05/2019
Test location:
Chicago:
Lat: 41.85, Long: -87.64999999999998
x: 65.67111111111113, y: 95.17492654697409
"""
import math

TILE_SIZE = 256


# Tested with coordinates of Chicago | website: https://developers.google.com/maps/documentation/javascript/coordinates
def get_world_coordinates(lat, lon):
    sin_y = math.sin(lat * math.pi/180)
    sin_y = min(max(sin_y, -0.9999), 0.9999)

    x = TILE_SIZE * (0.5 + lon/360)
    y = TILE_SIZE * (0.5 - math.log((1 + sin_y) / (1 - sin_y), math.e)/(4 * math.pi))

    coordinates = [x, y]
    return coordinates


# w1 and w2 in radians
def get_enemy_location(x1, y1, x2, y2, w1, w2):
    if (math.tan(w1) - math.tan(w2)) != 0:
        y = (x1 - x2 + y1*math.tan(w1) - y2*math.tan(w2))/(math.tan(w1) - math.tan(w2))
    else:
        y = (x1 - x2 + y1*math.tan(w1) - y2*math.tan(w2))/(math.tan(w1) - math.tan(w2) + 0.000001)
    x = x1 + (y1 - y)*math.tan(w1)
    res = [x, y]
    return res


# Tested ok with chicago coordinates
def inverse_mercator(x, y):
    lng = (x/256 * 360) - 180
    n = math.pi - (2 * math.pi) * (y / 256)
    lat = ((180 / math.pi) * math.atan(0.5 * (math.exp(n) - math.exp(-n))))
    loc = [round(lat, 6), round(lng, 6)]
    return loc


def convert_to_radians(degree):
    radians = float(degree) * (math.pi/180)
    return radians
