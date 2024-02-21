from GetTileValuesFromBoundingBox import TileCoordinateConverter
from OpenStreetMapTilesDownload import OpenStreetMapTilesDownload
from DownloadPanoraImage import LookAroundImageDownloaderFromTile
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
    # Get title coordinates from bounding box
    Tiles = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)

    # Get the total number of tiles
    total_tiles = len(Tiles.get_tiles_in_bbox())
    print(f'Number of tiles in the bounding box: {total_tiles}')
    PanoImage = LookAroundImageDownloaderFromTile()

    # Initialize a counter
    counter = 0

    print("Starting to Download Images")
    for i in Tiles.get_tiles_in_bbox():

        image = PanoImage.get_coverage_tile(tile_x=i[0], tile_y=i[1])
        print(len(image))
        print(image[172])
        print(i)
        break

        slippy_tile = OpenStreetMapTilesDownload(debug=False)
        url = slippy_tile.download_tile(17, i[0], i[1])

        PanoImage.download_panorama_face(image[0], url, i[0], i[1])



        # Increment the counter and print the progress
        counter += 1
        print(f'Downloaded {counter} out of {total_tiles} Image pairs.')



        # Makes sure this is run at the last iteration of the loop
        if counter == total_tiles:
            PanoImage.save_data()
            print("#######################################################")
            print("Download Completed")
            print("Downloading a total of ", counter*4, " images")
            print(f"Downloaded a total of {counter} tiles")
            print("#######################################################")

            break



if __name__ == "__main__":
    main()
