import osmium as osm
from PathAStar.Node import Node
import networkx as nx
from PathAStar.NodeLocator import NodeLocator

import networkx as nx
from heapq import heappush, heappop


def heuristic(node1, node2, graph):
    """
    Calculates the Haversine distance between two nodes as a heuristic for A* algorithm
    """
    lat1, lon1 = graph.nodes[node1]['latitude'], graph.nodes[node1]['longitude']
    lat2, lon2 = graph.nodes[node2]['latitude'], graph.nodes[node2]['longitude']
    return NodeLocator.haversine(lat1, lon1, lat2, lon2)


def find_shortest_path(graph, start_node, end_node):
    open_list = []
    closed_list = set()
    g_scores = {node: float('inf') for node in graph.nodes}
    g_scores[start_node] = 0
    parents = {node: None for node in graph.nodes}

    heappush(open_list, (0, start_node))

    while open_list:
        current_node = heappop(open_list)[1]

        if current_node == end_node:
            path = [end_node]
            while parents[current_node] is not None:
                current_node = parents[current_node]
                path.append(current_node)
            path.reverse()
            return path

        closed_list.add(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor in closed_list:
                continue

            tentative_g_score = g_scores[current_node] + graph[current_node][neighbor]['weight']

            if neighbor not in [node for score, node in open_list]:
                heappush(open_list, (tentative_g_score + heuristic(neighbor, end_node, graph), neighbor))
            elif tentative_g_score >= g_scores[neighbor]:
                continue

            parents[neighbor] = current_node
            g_scores[neighbor] = tentative_g_score

    return None


# Create an OSM handler
class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.nodes = {}

    def node(self, node):
        # Create a Node instance for each OSM node
        lat = node.location.lat
        lon = node.location.lon
        node_id = node.id
        osmnode = Node(lat, lon, node_id)
        osmnode.set_tags(node.tags)
        self.nodes[node_id] = osmnode


# Parse the PBF file
# Parse the PBF file
handler = OSMHandler()
with osm.Reader("bounding_box_map_aalborg.osm.pbf") as reader:
    scanner = osm.apply(reader, handler)
    for _ in scanner:
        pass

# Create a graph from the parsed OSM data
graph = nx.Graph()
for node in handler.nodes.values():
    graph.add_node(node.node_id, latitude=node.latitude, longitude=node.longitude)
    # Add edges between neighboring nodes based on OSM data

# Create a NodeLocator instance
node_locator = NodeLocator(graph)

# Find the closest nodes to the start and end points
start_lat, start_lon = 51.5072, 0.1275  # London
end_lat, end_lon = 48.8566, 2.3522  # Paris
start_node = node_locator.find_closest_node(start_lat, start_lon)
end_node = node_locator.find_closest_node(end_lat, end_lon)

# Perform pathfinding (e.g., using A* algorithm)
path = find_shortest_path(graph, start_node, end_node)
# path is a list of node IDs representing the shortest path