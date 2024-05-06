import pandas as pd
from NodeLocator import NodeLocator
from osm_to_graph import OSMToGraph


def get_image_data_from_graph(csv_file_path):
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm")
    drivable_graph = osm_to_graph.drivable_graph

    NodeFinder = NodeLocator(drivable_graph)

    data_frame = pd.read_csv(csv_file_path)

    # Remove duplicates from the DataFrame based on 'ID' column
    data_frame = data_frame.drop_duplicates(subset=['ID'])

    print("length of data frame after removing dup", len(data_frame))

    # Print the first 5 rows of the data frame
    print(data_frame.head())

    # get the headers of the data frame
    print(data_frame.columns)
    print(data_frame[['Latitude', 'Longitude']].values)

    # Create node match data frame
    node_match = pd.DataFrame(columns=['Node ID', 'Latitude', 'Longitude'])

    counter = 0
    for x, y in zip(data_frame['Latitude'], data_frame['Longitude']):

        node_id = NodeFinder.find_closest_node(float(x), float(y))
        node_match = pd.concat([node_match, pd.DataFrame({'Node ID': [node_id], 'Latitude': [y], 'Longitude': [x]})],
                               ignore_index=True)
        counter += 1
        print(f"Processed {counter} images")

    # Save the node match data frame to a CSV file
    node_match.to_csv("NodeMatch.csv", index=False)


if __name__ == "__main__":
    get_image_data_from_graph("ImageMetaDataSet.csv")
