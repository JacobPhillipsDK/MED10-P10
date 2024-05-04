import geojson

# Load the GeoJSON file
with open('../osm_data.geojson') as f:
    data = geojson.load(f)


ways = []

# Iterate through features and extract way information
for feature in data['features']:
    if feature['geometry']['type'] == 'LineString':
        way_id = feature['properties']['@id']
        node_coords = feature['geometry']['coordinates']
        tags = feature['properties'].get('tags', {})
        ways.append({
            'id': way_id,
            'node_coords': node_coords,
        })

# Now you have a dictionary of nodes and an array of ways
# You can create a graph by connecting nodes based on the way information
# Or you can search/filter the data based on your requirements

# print("Number of ways:", len(ways))
#
# # print the first 5 ways
# for way in ways[:5]:
#     print(way)

import math


def euclidean_distance(node1, node2):
    """Calculate the Euclidean distance between two nodes."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def build_graph(ways):
    """Build a graph from the list of ways."""
    graph = {}
    for way in ways:
        for i in range(len(way['node_coords']) - 1):
            node1 = tuple(way['node_coords'][i])  # Convert list to tuple
            node2 = tuple(way['node_coords'][i + 1])  # Convert list to tuple
            if node1 not in graph:
                graph[node1] = []
            if node2 not in graph:
                graph[node2] = []
            graph[node1].append((node2, euclidean_distance(node1, node2)))
            graph[node2].append((node1, euclidean_distance(node1, node2)))
    return graph



def a_star(graph, start, goal):
    """A* algorithm to find the shortest path between start and goal."""
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}

    while open_set:
        current = min(open_set, key=lambda node: f_score.get(node, float('inf')))
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        open_set.remove(current)
        for neighbor, cost in graph[current]:
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    return None


def find_nearest_node(graph, target):
    """Find the nearest node in the graph to the target coordinates."""
    min_dist = float('inf')
    nearest_node = None
    for node in graph.keys():
        dist = euclidean_distance(node, target)
        if dist < min_dist:
            min_dist = dist
            nearest_node = node
    return nearest_node

# Convert GeoJSON data to graph
graph = build_graph(ways)

# jacob house
start_lat, start_lon = 57.048028567059944, 9.928551711992268
# Comwell Hvide Hus Aalborg
goal_lat, goal_lon = 57.04256558551458, 9.910990256435174

# Find the nearest nodes to the start and end points
start_point = find_nearest_node(graph, (start_lat, start_lon))
end_point = find_nearest_node(graph, (goal_lat, goal_lon))

# Example usage: find the shortest path between the nearest nodes
shortest_path = a_star(graph, start_point, end_point)
print("Shortest Path:", shortest_path)
