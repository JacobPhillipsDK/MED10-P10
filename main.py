from GetTileValuesFromBoundingBox import TileCoordinateConverter
from OpenStreetMapTilesDownload import OpenStreetMapTilesDownload
from DownloadPanoraImage import LookAroundImageDownloaderFromTile
from DownloadPanoraImage import download_func_with_downloader, download_faces, split_list
from CreateDataSet import CreateImageMetaData
import os

# Bounding box coordinates
# Numbers are taken from openstreetmap where the bounding box is defined by the top-left and bottom-right coordinates
# top_left_lat = 57.0516
# top_left_lon = 9.9142
# bottom_right_lat = 57.0425
# bottom_right_lon = 9.9348


top_left_lat = 57.0537
top_left_lon = 9.9104
bottom_right_lat = 57.0393
bottom_right_lon = 9.9331


def main():
    # Get title coordinates from bounding box
    Tiles = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)

    # Get the total number of tiles
    total_tiles = len(Tiles.get_tiles_in_bbox())
    print(f'Number of tiles in the bounding box: {total_tiles}')

    Downloader = LookAroundImageDownloaderFromTile(debug=False)

    image_counter = 0

    tiles_list = []
    # We can check total images of the bounding box
    for i in range(total_tiles):
        tiles = Downloader.get_coverage_tile(Tiles.get_tiles_in_bbox()[i][0], Tiles.get_tiles_in_bbox()[i][1])
        image_counter += len(tiles)
        tiles_list.append((Tiles.get_tiles_in_bbox()[i][0], Tiles.get_tiles_in_bbox()[i][1]))

    print("Total number of images in the bounding box: ", image_counter)
    print(
        f'Found {total_tiles} tiles, start at {Tiles.get_tiles_in_bbox()[0]} and end at {Tiles.get_tiles_in_bbox()[-1]}')




if __name__ == "__main__":
    main()
    # folder = os.listdir("TestFolder/heic")
    # # We can check how many folders are created
    # print(len(folder))
