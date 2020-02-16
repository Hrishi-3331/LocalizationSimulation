import random
import Calculations
import SimulationSetup as Setup
import json as json
from prediction import Prediction

riffle_range = 300
ns = int(input('Enter number of soldiers :'))
ne = int(input('Enter number of enemies :'))

soldiers = Setup.generate_soldiers(ns)
enemies = Setup.generate_enemies(ne)
set_points = []

for z in range(0, 10):
    predictions = []
    for x in range(0, 10):
        i = 0
        done = []
        el = len(enemies)
        sl = len(soldiers)
        while i < el:
            index = random.randint(0, sl - 1)
            rep = False

            for p in done:
                if p == index:
                    rep = True
                    break

            if not rep:
                soldiers[index].set_target(enemies[i])
                done.append(index)
                i = i + 1

        for soldier in soldiers:
            if soldier.get_target() is None:
                soldier.set_target(enemies[random.randint(0, el - 1)])

        # Obtaining azimuth :
        for soldier in soldiers:
            angle = Setup.calculate_true_angle(soldier)
            azimuth = angle  #+ random.random()*0.01745329# max error : 4 degrees
            soldier.set_azimuth(azimuth)

        # Start simulation
        i = 0
        n = len(soldiers)
        while i < n:
            soldier1 = soldiers[i]
            [x1, y1] = Setup.get_coordinates(soldier1)
            w1 = soldier1.get_azimuth()
            p = i + 1
            while p < n:
                soldier2 = soldiers[p]
                [x2, y2] = Setup.get_coordinates(soldier2)
                w2 = soldier2.get_azimuth()
                res = Calculations.get_enemy_location(x1, y1, x2, y2, w1, w2)
                location = Calculations.inverse_mercator(res[0], res[1])
                if res[0] > max(x1, x2):
                    d = Setup.get_distance(location[1], location[0], soldier1.get_longitude(), soldier1.get_latitude())
                    if d < 300:
                        temp = Prediction(location[1], location[0])
                        predictions.append(temp)
                p = p + 1
            i = i + 1

    l = len(predictions)
    for j in range(0, l):
        prediction1 = predictions[j]
        for k in range(j + 1, l):
            prediction2 = predictions[k]
            if prediction1.equals(prediction2):
                prediction1.power_up()
                prediction2.make_redundant()

    for prediction in predictions:
        if prediction.get_redundancy():
            predictions.remove(prediction)

    sorted_predictions = sorted(predictions, key=lambda x: x.power, reverse=True)

    correct_predictions = []
    for enemy in enemies:
        lat = enemy.get_latitude()
        lon = enemy.get_longitude()
        for prediction in sorted_predictions:
            lat2 = prediction.get_latitude()
            lon2 = prediction.get_longitude()
            if lon2 == lon and lat2 == lat:
                correct_predictions.append(prediction)

    for j in range(0, len(sorted_predictions) - 1):
        prediction1 = sorted_predictions[j]
        if prediction1.power != 0:
            for i in range(j+1, len(sorted_predictions) - 1):
                prediction2 = sorted_predictions[i]
                if prediction1.equals(prediction2):
                    prediction1.power = prediction1.get_power() + prediction2.get_power()
                    prediction2.power = 0

    for prediction in sorted_predictions:
        if prediction.power > 0:
            set_points.append(prediction)

    for j in range(0, len(set_points)):
        prediction1 = set_points[j]
        if prediction1.power != 0:
            for i in range(j+1, len(set_points)):
                prediction2 = set_points[i]
                if prediction1.equals(prediction2):
                    prediction1.power = prediction1.get_power() + prediction2.get_power()
                    prediction2.power = 0

    new_set_points = []

    for prediction in set_points:
        if prediction.power > 0:
            new_set_points.append(prediction)

    set_points.clear()
    set_points = new_set_points

    set_points = sorted(set_points, key=lambda x: x.power, reverse=True)
    f = set_points[0].power
    for k in range(0, len(set_points)):
        set_points[k].prob = set_points[k].power/f

    prediction_result = []
    i = 0
    for prediction in set_points:
        if prediction.prob > 0.2:
            prediction_result.append(prediction)

    print("\n\nPredictions : Iteration " + str(z) + "\n\n")
    for point in set_points:
        print(str(point.get_probability()) + ', ' + str(point.get_latitude()) + ', ' + str(point.get_longitude()))

    print("\n\n")

    features = []
    i = 0
    for enemy in enemies:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    enemy.get_longitude(),
                    enemy.get_latitude()
                ]
            },
            "properties": {
                "title": 'Enemy' + str(i),
                "icon": "monument"
            }
        }
        features.append(temp)
        i = i + 1

    enemy_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/enemies.geojson', 'w') as outfile:
        json.dump(enemy_data, outfile)

    features = []
    i = 0
    for soldier in soldiers:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    soldier.get_longitude(),
                    soldier.get_latitude()
                ]
            },
            "properties": {
                "title": 'Soldier' + str(i),
                "icon": "monument"
            }
        }
        features.append(temp)
        i = i + 1

    soldier_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/soldiers.geojson', 'w') as outfile:
        json.dump(soldier_data, outfile)

    features = []
    i = 0
    for prediction in prediction_result:
        temp = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    prediction.get_longitude(),
                    prediction.get_latitude()
                ]
            },
            "properties": {
                "title": 'Prediction' + str(i),
                "icon": "monument",
                "mag": prediction.get_power()
            }
        }
        features.append(temp)
        i = i + 1

    prediction_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/predictions' + str(z) + '.geojson', 'w') as outfile:
        json.dump(prediction_data, outfile)

    features = []
    for soldier in soldiers:
        coordinates = [
            [soldier.get_longitude(), soldier.get_latitude()],
            [soldier.get_target().get_longitude(), soldier.get_target().get_latitude()]
        ]
        feature = {
            'type': 'Feature',
            'geometry': {
                "type": "LineString",
                "coordinates": coordinates
            }
        }
        features.append(feature)

    shoot_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('./plots/shoots' + str(z) + '.geojson', 'w') as outfile:
        json.dump(shoot_data, outfile)
