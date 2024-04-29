class Node:
    """
        A node class for A* Pathfinding
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h + cost
    """

    def __init__(self, latitude: str, longitude: str, node_id=None, cost=0):
        self.latitude = latitude
        self.longitude = longitude
        self.node_id = node_id
        self.cost = cost  # Cost or weight associated with traveling to this node

        self.g = 0  # cost from start to current Node
        self.h = 0  # heuristic based estimated cost for current Node to end Node
        self.f = 0  # total cost of present node i.e. :  f = g + h + cost

        self.neighbors = []
        self.degree = 0

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

    # You can optionally include a set_cost method if you need to update the cost later
    def set_cost(self, cost):
        self.cost = cost
        self.calculate_total_cost()

    def metaNodeData(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "node_id": self.node_id,
            "cost": self.cost,
            "g": self.g,
            "h": self.h,
            "f": self.f,
            "neighbors": self.neighbors,
            "degree": self.degree
        }


    def __repr__(self):
        return f"Node({self.node_id}, ({self.latitude}, {self.longitude}), neighbors={[n.node_id for n in self.neighbors]})"