class Node:
    def __init__(self, latitude : str, longitude : str, node_id=None):
        self.latitude = latitude
        self.longitude = longitude
        self.node_id = node_id
        self.g = 0
        self.h = 0
        self.f = 0



