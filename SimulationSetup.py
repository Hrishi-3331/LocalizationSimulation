import random
from soldier import Soldier
from enemy import Enemy
import math
import Calculations as SimCalculator


def generate_soldiers(n):
    c_lat = 21.129
    c_lon = 79.056
    i = 0
    soldiers = []
    while i < n:
        lt_temp = c_lat + random.randint(1, 5)*0.0001 + random.randint(3, 6)*0.00001 + random.randint(1, 9)*0.000001
        ln_temp = c_lon + random.randint(1, 4)*0.0001 + random.randint(3, 9)*0.00001 + random.randint(1, 9)*0.000001
        soldier = Soldier(i, round(ln_temp, 6), round(lt_temp, 6))
        soldiers.append(soldier)
        i = i + 1
    return soldiers


def generate_enemies(n):
    c_lat = 21.129
    c_lon = 79.056
    i = 0
    enemies = []
    while i < n:
        lt_temp = c_lat + random.randint(2, 7)*0.0001 + random.randint(2, 4)*0.00001 + random.randint(1, 9)*0.000001
        ln_temp = c_lon + random.randint(6, 9)*0.0001 + random.randint(0, 7)*0.00001 + random.randint(1, 7)*0.000001
        enemy = Enemy(i, round(ln_temp, 6), round(lt_temp, 6))
        enemies.append(enemy)
        i = i + 1
    return enemies


def calculate_true_angle(soldier):
    lat = soldier.get_latitude()
    lon = soldier.get_longitude()
    sc = SimCalculator.get_world_coordinates(lat, lon)
    lat2 = soldier.get_target().get_latitude()
    lon2 = soldier.get_target().get_longitude()
    ec = SimCalculator.get_world_coordinates(lat2, lon2)
    xe = ec[0]
    ye = ec[1]
    xs = sc[0]
    ys = sc[1]
    if ys - ye != 0:
        phi = math.atan((xe-xs)/(ys - ye))
    else:
        phi = math.pi/2
    return phi


def get_coordinates(soldier):
    lat = soldier.get_latitude()
    lon = soldier.get_longitude()
    sc = SimCalculator.get_world_coordinates(lat, lon)
    return sc


def get_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(a)) * 1000, 2)


def get_random_error():
    a = random.random()
    if a < 0.5:
        return -1
    else:
        return 1