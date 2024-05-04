from OSMHandler import OSMHandler
from NodeLocator import NodeLocator
from PathAStar import AStar


# Define the main function
def main():
    debug_print = False

    osm_file_path = "../bounding_box_map_aalborg.osm"

    tags_to_search = ["footway", "highway"]
    handler = OSMHandler(tags_to_search, osm_file_path)

    # Call post_process after parsing the OSM file
    handler.add_neighbor_nodes()

    # Graph built from the OSM file
    graph = handler.graph
    locator = NodeLocator(graph)

    if debug_print:
        # number of nodes
        print("Number of nodes", len(graph.nodes))
        # number of edges
        print("Number of edges", len(graph.edges))

        print("graph.nodes.__class__", graph.nodes.__class__)

        first_5_nodes = list(handler.nodes.values())[::1]
        # print("graph.nodes.", graph.nodes[first_5_nodes[0].node_id])
        for node in first_5_nodes:
            print(node.get_node_data(return_json=True))

        print("Node locator example:")
        # print(locator.find_closest_node(56.9988, 10.1627).get_node_data(return_json=True))
        print(locator.find_closest_node(56.9988, 10.1627).node_id)

    # jacob house
    start_lat, start_lon = 57.048028567059944, 9.928551711992268
    # Comwell Hvide Hus Aalborg
    goal_lat, goal_lon = 57.04256558551458, 9.910990256435174
    #
    start_node_id = locator.find_closest_node(start_lat, start_lon).node_id
    end_node_id = locator.find_closest_node(goal_lat, goal_lon).node_id

    print("Start node ID:", start_node_id)
    print("Start node data:", handler.nodes[start_node_id].get_node_data(return_json=False))
    print("End node ID:", end_node_id)
    print("End node data:", handler.nodes[end_node_id].get_node_data(return_json=False))

    start_node = handler.nodes[start_node_id]
    end_node = handler.nodes[end_node_id]

    astar = AStar(graph)
    path = astar.search(start_node, end_node)
    if path:
        print("Path found:")
        for node in path:
            print(node.metaNodeData())
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
