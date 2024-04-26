import numpy as np
from pyrosm import OSM
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


def euclidean_distance(node1, node2):
    """Calculate the Euclidean distance between two nodes."""
    return np.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)


def find_nearest_node(coord, road_network):
    """Find the nearest node in the road network to the given coordinates."""
    # Convert the road network to a projected CRS before calculating distances
    road_network_projected = road_network.to_crs("EPSG:3395")  # WGS 84 / World Mercator
    nearest_node = road_network_projected.geometry.distance(Point(coord)).idxmin()
    return nearest_node

def astar_search(start, goal, road_network):
    """Implement the A* search algorithm."""
    start_node = find_nearest_node(start, road_network)
    goal_node = find_nearest_node(goal, road_network)

    open_set = {start_node}
    closed_set = set()
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: euclidean_distance(start, goal)}

    while open_set:
        current = min(open_set, key=lambda node: f_score.get(node, float('inf')))
        if current == goal_node:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            # Convert node indices to coordinates
            path_coords = []
            for node in path:
                geom = road_network.loc[node, 'geometry']
                if geom.geom_type == 'MultiLineString':
                    path_coords.extend([xy for line in geom.geoms for xy in line.coords])
                else:
                    path_coords.extend(list(geom.coords))
            return path_coords

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in road_network.loc[current].dropna():
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + euclidean_distance(current, neighbor)

            if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                if neighbor not in open_set:
                    open_set.add(neighbor)

    return None  # No path found



# Load OSM data
aalborg_data = "output.osm.pbf"
osm = OSM(aalborg_data)

# - `'walking'` - `'cycling'` - `'driving'` - `'driving+service'` - `'all'`.

# get road map
drive_net = osm.get_network(network_type="all")

# Define start and end coordinates

start = (57.05263597716393, 9.917605413075808)
goal = (57.044436720148816, 9.916592865893952)

# Run A* search algorithm
path = astar_search(start, goal, drive_net)

# first coordinate
print("First coordinate", path[0])
# last coordinate
print("Last coordinate", path[-1])
# total number of coordinates
print("Total number of coordinates", len(path))


# # return the coordinates of the path as geojson
# path_gdf = gpd.GeoDataFrame(geometry=[Point(xy) for xy in path])
#
# # Save the path to a GeoJSON file
# path_gdf.to_file("path.geojson", driver='GeoJSON')
#
#
