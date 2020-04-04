class Prediction:

    def __init__(self, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.power = 0
        self.prob = 1
        self.redundant = False

    def power_up(self):
        self.power = self.power + 1

    def get_power(self):
        return self.power

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def equals(self, prediction):
        if self.latitude - prediction.latitude == 0 and self.longitude - prediction.longitude == 0:
            return True
        else:
            return False

    def make_redundant(self):
        self.redundant = True

    def get_redundancy(self):
        return self.redundant

    def get_probability(self):
        return self.prob
