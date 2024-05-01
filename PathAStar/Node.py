import json
import math
from typing import List, Any
from NodeLocator import NodeLocator
import osmium
from geopy.geocoders import Nominatim


class Node():
    """
        A node class for A* Pathfinding
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h + cost
    """

    def __init__(self, latitude: float, longitude: float, node_id, cost=0):
        self.latitude = latitude
        self.longitude = longitude
        self.node_id = node_id
        self.cost = cost  # Cost or weight associated with traveling to this node

        self.g = 0  # cost from start to current Node
        self.h = 0  # heuristic based estimated cost for current Node to end Node
        self.f = 0  # total cost of present node i.e. :  f = g + h + cost

        self.tags = {}

        self.include_address = False

        self.neighbors = []
        self.parent = None  # Add this line

    def random_cost(self):
        import random
        self.set_cost(random.randint(1, 10))

    def set_g(self, g):
        self.g = g

    def set_h(self, h):
        self.h = h

    def calculate_total_cost(self):
        """
        Calculate the total cost f for this node
        f = g + h + cost
        """
        self.f = self.g + self.h + self.cost

    def set_cost(self, cost):
        self.cost = cost
        self.calculate_total_cost()

    def set_tags(self, node_tags):
        self.tags = dict(node_tags)

    def metaNodeData(self) -> dict:
        return {
            "node_id": self.node_id,
            "location": {"latitude ": self.latitude, "longitude": self.longitude},
            "cost": self.cost,
            "g": self.g,
            "h": self.h,
            "f": self.f,
            "neighbors": self.get_neighbors(),
            "parent": self.parent.node_id if self.parent else None  # Add this line
        }

    @staticmethod
    def get_address(self, latitude, longitude):
        geolocator = Nominatim(user_agent="PathAStar")
        location = geolocator.reverse([latitude, longitude], exactly_one=True)
        return location.address if location else "No address found."

    def get_node_data(self, return_json=False):
        node_data = {
            "node_id": self.node_id,
            "location": {"latitude ": self.latitude, "longitude": self.longitude},
            "cost": self.cost,
            "neighbors": self.get_neighbors(),
            "address": self.get_address(self.latitude, self.longitude) if self.include_address else "set include_address to True to include address in the output.",
            "tags": self.tags,
            "parent": self.parent.node_id if self.parent else None  # Add this line
        }
        if return_json:
            return json.dumps(node_data, indent=4, ensure_ascii=False)
        else:
            return node_data

    def get_neighbors(self) -> list:
        return [neighbor.node_id for neighbor in self.neighbors]

    def heuristic(self, end_node):
        """Euclidean distance heuristic"""
        return math.sqrt((self.latitude - end_node.latitude) ** 2 + (self.longitude - end_node.longitude) ** 2)


if __name__ == "__main__":
    # test example of creating a node
    node = Node(57.048, 9.918, 1, 10)
    print(node.metaNodeData())