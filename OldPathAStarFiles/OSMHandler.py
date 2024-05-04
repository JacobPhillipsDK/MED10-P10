import osmium
import networkx as nx
from collections import defaultdict
from Node import Node


class OSMHandler(osmium.SimpleHandler):
    def __init__(self, tags, osm_file):
        super(OSMHandler, self).__init__()
        self.graph = nx.Graph()
        self.nodes = {}
        self.node_connectivity = defaultdict(list)
        self.debug = False

        self.tags = tags
        self.load_file(osm_file)

    def load_file(self, osm_filename):
        self.apply_file(osm_filename, locations=True, idx='flex_mem')

    @staticmethod
    def filter_out(tag, value):
        # Define the tags you want to filter out
        filter_out_tags = [("highway", "traffic_signals"), ("highway", "emergency_access_point"),
                           ("highway", "elevator"),
                           ("highway", "elevator"), ("highway", "bus_stop"), ("highway", "service"),
                           ("highway", "street_lamp")]
        return (tag, value) in filter_out_tags

    def node(self, n):
        for tag in self.tags:
            if tag in n.tags:
                if self.filter_out(tag, n.tags[tag]):
                    continue
            node = Node(n.location.lat, n.location.lon, n.id)
            node.random_cost()
            self.nodes[n.id] = node
            self.graph.add_node(node, latitude=n.location.lat, longitude=n.location.lon, cost=node.cost)
            node.set_tags(n.tags)

    def way(self, w):
        for tag in self.tags:
            if tag in w.tags:
                if self.filter_out(tag, w.tags[tag]):
                    continue
        nodes = [self.nodes[n.ref] for n in w.nodes]
        edges = list(zip(nodes, nodes[1:]))
        for n1, n2 in edges:
            self.graph.add_edge(n1, n2)
            self.node_connectivity[n1].append(n2)
            self.node_connectivity[n2].append(n1)

    def add_neighbor_nodes(self):
        for node, neighbor_nodes in self.node_connectivity.items():
            node.neighbors = neighbor_nodes
            node.degree = len(neighbor_nodes)
            if self.debug:
                print(f"Node {node.node_id} neighbors: {node.neighbors}")


if __name__ == "__main__":
    osm_file_path = "../bounding_box_map_aalborg.osm.pbf"  # Path to the .pbf file

    tags_to_search = ["footway", "highway"]

    handler = OSMHandler(tags_to_search, osm_file_path)

    # Call post_process after parsing the OSM file
    handler.add_neighbor_nodes()

    # Graph built from the OSM file
    graph = handler.graph

    # number of nodes
    print("Number of nodes", len(graph.nodes))
    # number of edges
    print("Number of edges", len(graph.edges))

