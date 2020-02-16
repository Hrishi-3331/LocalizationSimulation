class Soldier:

    def __init__(self, id_number, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.id_number = id_number
        self.target = None
        self.azimuth = None

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_id(self):
        return self.id_number

    def set_target(self, enemy):
        self.target = enemy

    def get_target(self):
        return self.target

    def set_azimuth(self, azimuth):
        self.azimuth = azimuth

    def get_azimuth(self):
        return self.azimuth
