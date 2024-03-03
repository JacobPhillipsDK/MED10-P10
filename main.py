from GetTileValuesFromBoundingBox import TileCoordinateConverter
from OpenStreetMapTilesDownload import OpenStreetMapTilesDownload
from DownloadPanoraImage import LookAroundImageDownloaderFromTile
from DownloadPanoraImage import download_func_with_downloader, download_faces, split_list, Pool, os, time
from CreateDataSet import CreateImageMetaData

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
    # # Get title coordinates from bounding box
    # tiles = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
    #
    # # Get the total number of tiles
    # total_tiles = len(tiles.get_tiles_in_bbox())
    # print(f'Number of tiles in the bounding box: {total_tiles}')
    #
    # Downloader = LookAroundImageDownloaderFromTile(debug=False)
    #
    # imagelen_counter = 0
    #
    # # tiles_list = []
    # # We can check total images of the bounding box
    # for i in range(total_tiles):
    #     tile = Downloader.get_coverage_tile(tiles.get_tiles_in_bbox()[i][0], tiles.get_tiles_in_bbox()[i][1])
    #     imagelen_counter += len(tile)
    #     # tiles_list.append((tiles.get_tiles_in_bbox()[i][0], tiles.get_tiles_in_bbox()[i][1]))
    #
    # print(
    #     f'Found {total_tiles} tiles, start at {tiles.get_tiles_in_bbox()[0]} and end at {tiles.get_tiles_in_bbox()[-1]}')
    # print("Total number of images in the bounding box: ", imagelen_counter)
    # #
    # # Downloading the images
    # #
    # # First we need to loop through the tiles
    #
    # # Number of processes you want to run concurrently
    # num_processes = os.cpu_count()

    image_counter = 0
    # Then we need to download the images from the tiles and save them to a folder and then repeat the downloading until all tiles are downlaoded
    metadata = CreateImageMetaData()


    # metadata.save_to_csv()

    #
    #     print(f"Downloading tile: {tile_xpos}/{tile_ypos}")
    #
    #     # Download the images
    #
    #     panos = Downloader.get_coverage_tile(tile_xpos, tile_ypos)
    #     image_counter += len(panos)
    #
    #     print(f'Got {len(panos) * 4} panoramas')
    #
    #     split_panos = split_list(panos, num_processes)
    #
    #     with Pool(num_processes) as pool:
    #         flat_panos = [item for sublist in split_panos for item in sublist]
    #         start_time = time.time()  # Start the timer
    #         pool.starmap(download_func_with_downloader,
    #                      [(panorama, Downloader, tile_xpos, tile_ypos) for panorama in flat_panos])
    #
    #         end_time = time.time()  # End the timer
    #
    #     print(f"Total time for downloading: {end_time - start_time} seconds")
    #     print(f'Image counter: {image_counter} of panos: {len(panos)*4}')
    #
    #     # download_tile = OpenStreetMapTilesDownload()
    #     # download_tile.download_tile(zoom=17, x=tile_xpos, y=tile_ypos)
    #
    # print("Total number of images downloaded from the bounding box: ", image_counter)
    # print("Total number of images found in the bounding box: ", imagelen_counter)


if __name__ == "__main__":
    main()
