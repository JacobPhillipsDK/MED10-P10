import pandas as pd
import osmnx as ox
from NodeLocator import NodeLocator
from osm_to_graph import OSMToGraph


def get_image_data_from_graph(csv_file_path):
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm")
    drivable_graph = osm_to_graph.get_graph()

    NodeFinder = NodeLocator(drivable_graph)
    print(NodeFinder.find_closest_node(57.03925715937763, 9.93170541875503))

    data_frame = pd.read_csv(csv_file_path)

    # Print the first 5 rows of the data frame
    print(data_frame.head())

    # get the headers of the data frame
    print(data_frame.columns)
    print(data_frame[['Latitude', 'Longitude']].values)

    # Create node match data frame
    node_match = pd.DataFrame(columns=['Node ID', 'Latitude', 'Longitude'])

    counter = 0
    for x, y in zip(data_frame['Latitude'], data_frame['Longitude']):
        if counter > 15:
            break
        node_id = ox.nearest_nodes(drivable_graph, x, y)
        print(f"x: {x}, y: {y}, node_id: {node_id}")
        if node_match.empty:
            node_match = pd.DataFrame({'Node ID': [node_id], 'Latitude': [x], 'Longitude': [y]})
        else:
            node_match = pd.concat(
                [node_match, pd.DataFrame({'Node ID': [node_id], 'Latitude': [x], 'Longitude': [y]})],
                ignore_index=True)
        counter += 1
        print(f"Processed {counter} images")

    # Save the node match data frame to a CSV file
    node_match.to_csv("NodeMatch.csv", index=False)


if __name__ == "__main__":
    get_image_data_from_graph("ImageMetaDataSetNoDup.csv")
