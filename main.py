from GetTileValuesFromBoundingBox import TileCoordinateConverter
from OpenStreetMapTilesDownload import OpenStreetMapTilesDownload
from DownloadPanoraImage import LookAroundImageDownloaderFromTile




# Bounding box coordinates
# Numbers are taken from openstreetmap where the bounding box is defined by the top-left and bottom-right coordinates
top_left_lat = 57.0516
top_left_lon = 9.9142
bottom_right_lat = 57.0425
bottom_right_lon = 9.9348




def main():
    # Get title coordinates from bounding box
    # Tiles are defined by x and y coordinates also known slippy map coordinates
    Tiles = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)

    # With the tiles now we can use those coordinates to find all the panorama images within the bounding box
    # The images are downloaded from lookaround ( Apple Maps )
    # This will download the first panorama image from the first tile
    image = LookAroundImageDownloaderFromTile(tile_x=Tiles.get_tiles_in_bbox()[0][0],
                                               tile_y=Tiles.get_tiles_in_bbox()[0][1])
    image.image_metaData()

    # Download the slippy map tiles from openstreetmap
    slippy_tile = OpenStreetMapTilesDownload(debug=True)
    slippy_tile.show_tile(17, Tiles.get_tiles_in_bbox()[0][0], Tiles.get_tiles_in_bbox()[0][1])

    # Download a panorama image from a specific tile
    image.download_panorama_face(image.panos[0], f"TestFolder/{image.panos[0].id}_{0}_{0}.heic", 0)


if __name__ == "__main__":
    main()
