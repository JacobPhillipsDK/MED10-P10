import osmnx as ox
import networkx as nx
from pyrosm_aalborg import PathPlot
from PathAStar import AStarSearch

# Parse the OSM XML data
graph = ox.graph_from_xml("../bounding_box_map_aalborg.osm", simplify=False)


drivable_graph = ox.project_graph(ox.utils_graph.truncate.largest_component(graph, strongly=True),
                                  to_crs="EPSG:4326")  # Project to EPSG:4326 for filtering


# Define a custom cost function for each path
def custom_cost(node1, node2):
    u = drivable_graph.nodes[node1]
    v = drivable_graph.nodes[node2]

    # Calculate the distance between the nodes
    distance = ((u['y'] - v['y']) ** 2 + (u['x'] - v['x']) ** 2) ** 0.5

    # Check if the 'highway' key exists in the edge data
    edge_data = drivable_graph.edges[(node1, node2, 0)]
    if 'highway' in edge_data:
        road_type = edge_data['highway']
        # Assign higher costs to certain highway types
        if road_type in ['motorway', 'trunk']:
            road_type_factor = 5  # Make motorways and trunk roads 5 times more expensive
        elif road_type == 'primary':
            road_type_factor = 3  # Make primary roads 3 times more expensive
        elif road_type == 'secondary':
            road_type_factor = 2  # Make secondary roads 2 times more expensive
        else:
            road_type_factor = 1  # Other road types have a factor of 1
    else:
        # Assign a default road type factor if 'highway' key is not present
        road_type_factor = 2

    # Check if the edge is marked as walkable
    if 'footway' in edge_data or 'pedestrian' in edge_data or 'path' in edge_data:
        # Assign the lowest cost factor to walkable paths
        road_type_factor = 0.5

    return distance * road_type_factor

# Modify the graph by assigning custom weights to the edges
for u, v, k, data in drivable_graph.edges(keys=True, data=True):
    data['weight'] = custom_cost(u, v)
    # print(data)


# Define the heuristic function (custom heuristic cost)
def heuristic(a, b):
    (x1, y1) = drivable_graph.nodes[a]['y'], drivable_graph.nodes[a]['x']
    (x2, y2) = drivable_graph.nodes[b]['y'], drivable_graph.nodes[b]['x']

    # Calculate the custom heuristic cost based on Euclidean distance
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5



# Define the start and end coordinates (longitude, latitude)
start_lng, start_lat = 57.048028567059944, 9.928551711992268
end_lng, end_lat = 57.04256558551458, 9.910990256435174

# Find the nearest nodes to the start and end coordinates
start_node = ox.nearest_nodes(drivable_graph, start_lat, start_lng)
end_node = ox.nearest_nodes(drivable_graph, end_lat, end_lng)

# Find the shortest path using A* with custom costs
# custom path a star here :
PathStar_object = AStarSearch(drivable_graph, start_node, end_node, heuristic, custom_cost)

path = PathStar_object.a_star_search()

print("Path:", path)

# Convert node IDs to coordinates
path_coords = [(drivable_graph.nodes[node]['y'], drivable_graph.nodes[node]['x']) for node in path]

print("Path coordinates:", path_coords)

# Calculate the total distance of the path
total_distance = sum(drivable_graph.get_edge_data(u, v)[0]['length'] for u, v in nx.utils.pairwise(path))

# Convert distance to kilometers
total_distance_km = total_distance / 1000

# Calculate the estimated time to walk the path (in seconds)
average_walking_speed_m_per_s = 1.4
estimated_time_s = total_distance / average_walking_speed_m_per_s

# Convert estimated time to minutes
estimated_time_min = estimated_time_s / 60

print(f"Total distance: {total_distance_km} km")
print(f"Estimated time: {estimated_time_min} minutes")

pathplot = PathPlot(path_coords, "../output.osm.pbf")
pathplot.plot()