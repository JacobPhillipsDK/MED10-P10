import osmium
import networkx as nx
from collections import defaultdict
from Node import Node

class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.graph = nx.Graph()
        self.nodes = {}
        self.node_connectivity = defaultdict(list)

        self.debug = False

    def node(self, n):
        node = Node(n.location.lat, n.location.lon, n.id)
        self.nodes[n.id] = node
        self.graph.add_node(node)


    def way(self, w):
        if 'highway' in w.tags:
            road_name = w.tags.get('name', 'Unknown')
            road_type = w.tags.get('highway', 'Unknown')
            nodes = [self.nodes[n.ref] for n in w.nodes]
            edges = list(zip(nodes, nodes[1:]))
            for n1, n2 in edges:
                self.graph.add_edge(n1, n2, name=road_name, road_type=road_type)
                self.node_connectivity[n1].append(n2)
                self.node_connectivity[n2].append(n1)
                if self.debug:
                    print(f"Node {n1.node_id} neighbors: {self.node_connectivity[n1]}")
                    print(f"Node {n2.node_id} neighbors: {self.node_connectivity[n2]}")

    def post_process(self):
        for node, neighbors in self.node_connectivity.items():
            node.neighbors = neighbors
            node.degree = len(neighbors)
            if self.debug:
                print(f"Node {node.node_id} neighbors: {node.neighbors}")


# Parse the OSM file and create the graph
osm_file = "../aalborg_map.osm"
handler = OSMHandler()
handler.apply_file(osm_file)
graph = handler.graph


# Print the number of nodes and edges
print("Number of nodes:", graph.number_of_nodes())
print("Number of edges:", graph.number_of_edges())


# print the first 10 nodes
print("First node:", list(graph.nodes())[:1])

# print the first 10 edges
print("First edge:", list(graph.edges())[:1])

# Get the node with a specific ID
