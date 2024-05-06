import osmnx as ox
from osm_to_graph import OSMToGraph
from NodeLocator import NodeLocator


# Define the heuristic function (custom heuristic cost)
def heuristic(graph, a, b):
    (x1, y1) = graph.nodes[a]['y'], graph.nodes[a]['x']
    (x2, y2) = graph.nodes[b]['y'], graph.nodes[b]['x']

    # Calculate the custom heuristic cost based on Euclidean distance
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def main():
    # Load the drivable graph of Aalborg
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm")
    drivable_graph = osm_to_graph.drivable_graph

    NodeFinder = NodeLocator(drivable_graph)

    image_lat = 57.05268563993586
    image_lon = 9.910611096550412

    print(f"node x and y: {image_lat}, {image_lon}")
    print("ox implementation", ox.nearest_nodes(drivable_graph, image_lat, image_lon))
    print("custom code", NodeFinder.find_closest_node(image_lat, image_lon))

    # Define the start and end coordinates (longitude, latitude)
    start_lng, start_lat = 57.048028567059944, 9.928551711992268
    end_lng, end_lat = 57.04256558551458, 9.910990256435174

    # Find the nearest nodes to the start and end coordinates
    # start_node = ox.nearest_nodes(drivable_graph, start_lat, start_lng)
    # end_node = ox.nearest_nodes(drivable_graph, end_lat, end_lng)

    start_node = NodeFinder.find_closest_node(start_lat, start_lng)
    end_node = NodeFinder.find_closest_node(end_lat, end_lng)


if __name__ == "__main__":
    main()
