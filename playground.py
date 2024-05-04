import requests

# Define your query
query = """
(
  way["highway"="primary"]({{bbox}});
  way["highway"="secondary"]({{bbox}});
  way["highway"="path"]({{bbox}});
  way["highway"="residential"]({{bbox}});
  way["highway"="unclassified"]({{bbox}});
  way["highway"="pedestrian"]({{bbox}});
  way["highway"="crossing"]({{bbox}});
  way["highway"="footway"]({{bbox}});
  way["highway"="tertiary"]({{bbox}});
  way["highway"="trunk"]({{bbox}});
  way["highway"="service"]({{bbox}});
);
out geom;
"""

# Define your bounding box
top_left_lat = 57.0516
top_left_lon = 9.9142
bottom_right_lat = 57.0425
bottom_right_lon = 9.9348

# Construct the bounding box string
bbox_str = f"{top_left_lon},{bottom_right_lat},{bottom_right_lon},{top_left_lat}"

# Define the Overpass API URL
overpass_url = "https://overpass-api.de/api/interpreter"

# Define the parameters
params = {
    "data": query.replace("{{bbox}}", bbox_str),
    "format": "json"
}

# Make the request
response = requests.get(overpass_url, params=params)

print(response.text)

# # Save the response to a file
# with open("osm_data.geojson", "w") as f:
#     f.write(response.text)
#
# print("Data downloaded successfully!")
