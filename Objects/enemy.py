class Enemy:

    def __init__(self, id_number, longitude, latitude):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.id_number = id_number

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_id(self):
        return self.id_number