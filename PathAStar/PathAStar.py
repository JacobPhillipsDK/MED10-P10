import osmium
import networkx as nx
from Node import Node

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.graph = nx.Graph()
        self.nodes = {}

    def node(self, n):
        self.nodes[n.id] = Node(n.location.lat, n.location.lon, n.id)

    def way(self, w):
        if 'highway' in w.tags:
            # Filter out specific road types
            if w.tags['highway'] in ['primary', 'secondary']:
                for i in range(len(w.nodes) - 1):
                    node1 = self.nodes[w.nodes[i].ref]
                    node2 = self.nodes[w.nodes[i+1].ref]
                    # Calculate custom weightings
                    weight = self.calculate_weight(node1, node2)
                    self.graph.add_edge(node1, node2, weight=weight)

    def calculate_weight(self, node1, node2):
        # Example: Custom weighting based on distance between nodes
        distance = self.calculate_distance(node1, node2)
        # You can define your own custom weighting function here
        # For example, you could use distance, road type, etc.
        return distance

    def calculate_distance(self, node1, node2):
        # Simple Euclidean distance calculation
        lat1, lon1 = node1.latitude, node1.longitude
        lat2, lon2 = node2.latitude, node2.longitude
        return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5

# Parse the OSM file and create the graph
osm_file = "your_osm_file.osm"
handler = OSMHandler()
handler.apply_file(osm_file)
graph = handler.graph
