"""
Created by Hrishikesh Ugale
10/05/2019
Test location:
Chicago:
Lat: 41.85, Long: -87.64999999999998
x: 65.67111111111113, y: 95.17492654697409
"""

import math
from Setup import Calculations as SimCalculator

'''input('Enter the coordinates : True loc, Predicted loc, Soldier loc')
arr = input()   # takes the whole line of n numbers
loc = list(map(float, arr.split(' ')))'''

with open("error", "r") as ins:
    array = []
    for line in ins:
        loc = list(map(float, line.split(' ')))

        lat = float(loc[4])
        lon = float(loc[5])
        sc = SimCalculator.get_world_coordinates(lat, lon)
        lat2 = float(loc[0])
        lon2 = float(loc[1])
        ec = SimCalculator.get_world_coordinates(lat2, lon2)
        xe = ec[0]
        ye = ec[1]
        xs = sc[0]
        ys = sc[1]
        if ys - ye != 0:
            true_phi = math.atan((xe - xs) / (ys - ye))
        else:
            true_phi = math.pi / 2

        lat = float(loc[4])
        lon = float(loc[5])
        sc = SimCalculator.get_world_coordinates(lat, lon)
        lat2 = float(loc[2])
        lon2 = float(loc[3])
        ec = SimCalculator.get_world_coordinates(lat2, lon2)
        xe = ec[0]
        ye = ec[1]
        xs = sc[0]
        ys = sc[1]
        if ys - ye != 0:
            calc_phi = math.atan((xe - xs) / (ys - ye))
        else:
            calc_phi = math.pi / 2

        error = true_phi - calc_phi

        print(math.degrees(true_phi))
        print(math.degrees(calc_phi))
        print(math.degrees(error))
        file1 = open("error report.txt", "a")  # append mode
        file1.write(line + ' ' + str(math.degrees(true_phi)) + ' ' + str(math.degrees(calc_phi)) + ' ' + str(math.degrees(error)))
        file1.close()
