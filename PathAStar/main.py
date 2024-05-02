from OSMHandler import OSMHandler
from NodeLocator import NodeLocator
from PathAStar import AStarPathfinder


# Define the main function
def main():
    debug_print = False

    osm_file_path = "../bounding_box_map_aalborg.osm"

    handler = OSMHandler()

    handler.apply_file(osm_file_path, locations=True, idx='flex_mem')

    # Call post_process after parsing the OSM file
    handler.add_neighbor_node()

    # Graph built from the OSM file
    graph = handler.graph
    locator = NodeLocator(graph)

    if debug_print:
        # number of nodes
        print("Number of nodes", len(graph.nodes))
        # number of edges
        print("Number of edges", len(graph.edges))

        print("graph.nodes.__class__", graph.nodes.__class__)

        first_5_nodes = list(handler.nodes.values())[:1]
        # print("graph.nodes.", graph.nodes[first_5_nodes[0].node_id])
        for node in first_5_nodes:
            print(node.get_node_data(return_json=True))

        print("Node locator example:")
        # print(locator.find_closest_node(56.9988, 10.1627).get_node_data(return_json=True))
        print(locator.find_closest_node(56.9988, 10.1627).node_id)

    # acob house
    start_lat, start_lon = 57.048028567059944, 9.928551711992268
    # Comwell Hvide Hus Aalborg
    goal_lat, goal_lon = 57.04256558551458, 9.910990256435174
    #
    start_node_id = locator.find_closest_node(start_lat, start_lon).node_id
    end_node_id = locator.find_closest_node(goal_lat, goal_lon).node_id
    #
    print("Start node ID:", start_node_id)
    print("End node ID:", end_node_id)

    #
    start_node = handler.nodes[start_node_id]
    end_node = handler.nodes[end_node_id]
    #
    astar = AStarPathfinder(graph)

    # # Find the path using the AStarPathfinder
    path = astar.find_path(start_node=start_node, end_node=end_node, is_drivable=False)
    #
    if path:
        print("Path found:")
        for node in path:
            print(node.metaNodeData())
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
