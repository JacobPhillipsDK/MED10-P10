import math


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def get_tiles_in_bbox(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, zoom):
    top_left_tile = deg2num(top_left_lat, top_left_lon, zoom)
    bottom_right_tile = deg2num(bottom_right_lat, bottom_right_lon, zoom)

    tiles = []
    for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
        for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
            tiles.append((x, y))

    return tiles


# Define the bounding box (top left and bottom right coordinates)
top_left_lat = 57.0516
top_left_lon = 9.9142
bottom_right_lat = 57.0425
bottom_right_lon = 9.9348

# Define the zoom level
zoom = 17

# Get all tiles within the bounding box
tiles = get_tiles_in_bbox(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, zoom)

# Print the tiles
for tile in tiles:
    print(tile)
    # sort list
    tiles.sort()
    # remove duplicates
    # print total sets of tiles

print(len(set(tiles)))
