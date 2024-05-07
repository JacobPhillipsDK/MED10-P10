import osmnx as ox
import  pandas as pd


class OSMToGraph:
    def __init__(self, file_path):

        self.graph = ox.graph_from_xml(file_path, simplify=False)
        self.drivable_graph = ox.project_graph(ox.utils_graph.truncate.largest_component(self.graph, strongly=True),
                                               to_crs="EPSG:4326")  # Project to EPSG:4326 for filtering

    # Define a custom cost function for each path

    # Super Class weight function
    # City infrastructure
    # Residential Zone
    # Commercial Zone
    # Entertainment Zone
    # Nature
    # Harbour
    # Culture

    # City infrastructure, Residential Zone, Commercial Zone, Entertainment Zone, Nature, Harbour, Culture
    def initialize_custom_data(self, file_pathj):
        # Read custom data from CSV file and store it as node attributes
        try:
            # Read custom data from CSV file and store it as node attributes
            custom_data_df = pd.read_csv(file_pathj)  # Replace "custom_data.csv" with your CSV file path
            # Iterate over rows in the DataFrame and add custom data as attributes to nodes
            for index, row in custom_data_df.iterrows():
                node_id = row['Node ID']

                custom_values = {
                    'city_infrastructure': row['City infrastructure'],
                    'residential_zone': row['Residential Zone'],
                    'commercial_zone': row['Commercial Zone'],
                    'entertainment_zone': row['Entertainment Zone'],
                    'nature': row['Nature'],
                    'harbour': row['Harbour'],
                    'culture': row['Culture']
                }
                # Add custom data as attributes to nodes
                self.drivable_graph.nodes[node_id].update(custom_values)
        except FileNotFoundError:
            print("Error: Could not read the custom data CSV file.")
            return



    def custom_cost(self, node1, node2):
        u = self.drivable_graph.nodes[node1]
        v = self.drivable_graph.nodes[node2]


        # Calculate the distance between the nodes
        distance = ((u['y'] - v['y']) ** 2 + (u['x'] - v['x']) ** 2) ** 0.5

        # Check if the 'highway' key exists in the edge data
        edge_data = self.drivable_graph.edges[(node1, node2, 0)]
        if 'highway' in edge_data:
            road_type = edge_data['highway']
            # Assign higher costs to certain highway types
            if road_type in ['motorway', 'trunk']:
                road_type_factor = 10  # Make motorways and trunk roads 5 times more expensive
            elif road_type == 'primary':
                road_type_factor = 3  # Make primary roads 3 times more expensive
            elif road_type == 'secondary':
                road_type_factor = 2  # Make secondary roads 2 times more expensive
            else:
                road_type_factor = 2  # Other road types have a factor of 1
        else:
            # Assign a default road type factor if 'highway' key is not present
            road_type_factor = 2

        # Check if the edge is marked as walkable
        if 'footway' in edge_data or 'pedestrian' in edge_data or 'path' in edge_data:
            # Assign the lowest cost factor to walkable paths
            road_type_factor = 10

        return distance * road_type_factor


    def get_graph(self):
        return self.drivable_graph



    def modify_graph(self):
        # Modify the graph by assigning custom weights to the edges
        for u, v, k, data in self.drivable_graph.edges(keys=True, data=True):
            data['weight'] = self.custom_cost(u, v)
            # print(data)


if __name__ == "__main__":
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm")
    osm_to_graph.modify_graph()
    drivable_graph = osm_to_graph.get_graph()
    # osm_to_graph.initialize_custom_data("ImageMetaDataSetWithNodeID.csv")
    print(drivable_graph.nodes(data=True))
    # print(drivable_graph.edges(data=True))

