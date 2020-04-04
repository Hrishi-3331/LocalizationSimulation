"""
Created by Hrishikesh Ugale
10/05/2019
Test location:
Chicago:
Lat: 41.85, Long: -87.64999999999998
x: 65.67111111111113, y: 95.17492654697409
"""

import random
from Objects.soldier import Soldier
from Objects.enemy import Enemy
import math
from Setup import Calculations as SimCalculator


# Generate Soldiers at random locations on battlefield
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


# Generate enemies at random locations on battlefield
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


# Calculate angle w.r.t north using trigonometric calculations.
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


# Returns gps coordinates of soldier
def get_coordinates(soldier):
    lat = soldier.get_latitude()
    lon = soldier.get_longitude()
    sc = SimCalculator.get_world_coordinates(lat, lon)
    return sc


# Returns distance between two locations in meters
def get_distance(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(a)) * 1000, 2)


# Returns random positive and negative errors
def get_random_error():
    a = random.random()
    if a < 0.5:
        return -1
    else:
        return 1
