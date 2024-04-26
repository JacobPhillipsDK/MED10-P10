# import osmnx as ox
#
# # Load the OSM data from a file
# osm_aalborg_data = "bounding_box_map_aalborg.osm"
# graph = ox.graph_from_xml(osm_aalborg_data, simplify=False)
#
# # Filter the graph to include only walkable paths
# walkable_graph = ox.project_graph(ox.utils_graph.get_largest_component(graph), to_crs="EPSG:4326")  # Project to EPSG:4326 for filtering
#
# # Convert the graph to geopandas GeoDataFrames
# gdf_nodes, gdf_edges = ox.graph_to_gdfs(walkable_graph, nodes=True, edges=True, node_geometry=False, fill_edge_geometry=True)
#
# # Create a new graph from the GeoDataFrames
# walkable_graph = ox.graph_from_gdfs(gdf_nodes, gdf_edges)
#
# # If you want the graph to be directed
# walkable_graph = walkable_graph.to_directed()
#
# # Plot the walkable paths
# ox.plot_graph(walkable_graph)


