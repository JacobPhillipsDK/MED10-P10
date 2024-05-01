import osmium
import networkx as nx
from collections import defaultdict
from Node import Node
import json


class OSMHandler(osmium.SimpleHandler):
    def __init__(self):
        super(OSMHandler, self).__init__()
        self.graph = nx.Graph()
        self.nodes = {}
        self.node_connectivity = defaultdict(list)
        self.debug = False
        self.tag_filtering = True
        self.DRIVABLE_TAGS = {
            'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential',
                        'service', 'living_street', 'pedestrian'],
            'area': ['no'],  # Exclude areas
            'access': ['yes', 'permissive']  # Exclude features with restricted access
        }

    def node(self, n):
        node = Node(n.location.lat, n.location.lon, n.id)
        node.random_cost()
        self.nodes[n.id] = node
        self.graph.add_node(node, latitude=n.location.lat, longitude=n.location.lon, cost=node.cost)
        node.set_tags(n.tags)

    def way(self, w):
        drivable = False
        if self.tag_filtering:
            for tag in w.tags:
                if tag.k in self.DRIVABLE_TAGS and tag.v in self.DRIVABLE_TAGS[tag.k]:
                    drivable = True
                    print(f"Way {w.id} is drivable")
                    break

            if drivable:
                nodes = [self.nodes[n.ref] for n in w.nodes if n.ref in self.nodes]
                edges = list(zip(nodes, nodes[1:]))
                for n1, n2 in edges:
                    self.graph.add_edge(n1, n2)
                    self.node_connectivity[n1].append(n2)
                    self.node_connectivity[n2].append(n1)
                print("nodes", nodes)

        if not self.tag_filtering:
            nodes = [self.nodes[n.ref] for n in w.nodes]
            edges = list(zip(nodes, nodes[1:]))
            for n1, n2 in edges:
                self.graph.add_edge(n1, n2)
                self.node_connectivity[n1].append(n2)
                self.node_connectivity[n2].append(n1)


def relation(self, r):
    pass


def add_neighbor_node(self):
    for node, neighbor_nodes in self.node_connectivity.items():
        node.neighbors = neighbor_nodes
        node.degree = len(neighbor_nodes)
        if self.debug:
            print(f"Node {node.node_id} neighbors: {node.neighbors}")


# def get_node_by_id(self, graph, node_id):
#     for node in graph.nodes.values():
#         if node.node_id == node_id:
#             return node
#     return None


if __name__ == "__main__":
    osm_file_path = "../bounding_box_map_aalborg.osm.pbf"  # Path to the .pbf file

    handler = OSMHandler()
    handler.apply_file(osm_file_path, locations=True, idx='flex_mem')

    # Call post_process after parsing the OSM file
    handler.add_neighbor_node()

    # Graph built from the OSM file
    graph = handler.graph

    # print("Graph nodes:", graph.nodes)

    # number of nodes
    print("Number of nodes", len(graph.nodes))
    # number of edges
    print("Number of edges", len(graph.edges))

    # first node
    # print(list(handler.nodes[0]

    print(graph.nodes.values().__class__)

    # print the first 5 nodes

    first_5_nodes = [node for node in list(handler.nodes.values())[:1]]
    for i in first_5_nodes:
        print(i.get_node_data(return_json=True))

    # # get first 10 nodes
    # first_5_nodes = [node for node in list(handler.nodes.values())]
    #
    # for i in first_5_nodes:
    #     print(i.get_node_data(return_json=True))

    # get node object by id
    # node = handler.get_node_by_id(handler.graph, 22760609)
    # print(node)
