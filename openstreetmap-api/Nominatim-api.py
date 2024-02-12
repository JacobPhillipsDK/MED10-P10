from geopy.geocoders import Nominatim

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Provide the address
address = "Rendsburggade 10a, 9000 Aalborg"

# Get the location (returns a Location object)
location = geolocator.geocode(address)

# Check if the location was found
if location:
    # Extract latitude and longitude from the location
    latitude, longitude = location.latitude, location.longitude

    # Print the result
    print(f"Address: {address}")
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print(f"Could not find GPS coordinates for the address: {address}")


import overpy

# Initialize the Overpass API
api = overpy.Overpass()

# Replace these with the actual latitude and longitude of your address
latitude = 57.0488
longitude = 9.9197

# Define a radius within which to search for nodes (adjust as needed)
radius = 50

# Construct the Overpass query to find nodes within the specified radius
query = f"""
    node(around:{radius},{latitude},{longitude});
    out;
"""

# Send the query and get the result
result = api.query(query)

# Check if any nodes were found
if result.nodes:
    node = result.nodes[0]  # Assuming the first node in the result is what you're looking for

    # Print the node information
    print(f"Node ID: {node.id}")
    print(f"Latitude: {node.lat}, Longitude: {node.lon}")
else:
    print(f"No node found near the specified coordinates.")


