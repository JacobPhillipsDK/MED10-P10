import time
from streetlevel import lookaround
from CreateDataSet import CreateImageMetaData
from geopy.geocoders import Nominatim
from multiprocessing import Pool


class LookAroundImageDownloaderFromTile(CreateImageMetaData):
    def __init__(self, zoom=0, debug=False):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.zoom = zoom  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
        self.panos = None
        self.MetaData = CreateImageMetaData()
        self.debug = debug

    def get_coverage_tile(self, tile_x, tile_y):
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)
        return self.panos

    def image_metaData(self, panorama) -> tuple:
        panos_ID = str(panorama.id)
        panos_build_ID = str(panorama.build_id)
        panos_lat = str(panorama.lat)
        panos_lon = str(panorama.lon)
        panos_date = str(panorama.date)

        if self.debug:
            print(f"""
               Got {len(self.panos)} panoramas. Here's one of them:
               ID: {panorama.id}\t\tBuild ID: {panorama.build_id}
               Latitude: {panorama.lat}\tLongitude: {panorama.lon}
               Capture date: {panorama.date}\tAddress: {"hello world"}
               """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, "hello"

    def download_panorama_face(self, panorama, url, tile_xpos, tile_ypos, zoom=None):

        panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, address = self.image_metaData(panorama)

        if zoom is None:
            zoom = self.zoom

        for face in range(0, 4):
            # address = self.get_gps_directions(panorama.lat, panorama.lon).replace(' ', '_').replace(',', '')
            image_path = f"{self.heic_path}/{panos_ID}_{face}.heic"
            lookaround.download_panorama_face(pano=panorama, path=image_path, face=face, zoom=zoom, auth=self.auth)

            self.MetaData.append_image_data(image_name=f"{panos_ID}_{face}",
                                            panos_ID=panos_ID,
                                            panos_build_ID=panos_build_ID,
                                            panos_lat=panos_lat,
                                            panos_lon=panos_lon,
                                            panos_date=panos_date,
                                            URL=url, tile_xpos=tile_xpos,
                                            tile_ypos=tile_ypos,
                                            address=address, face_value=face)

    def save_data(self):
        self.MetaData.save_to_csv()

    @staticmethod
    def get_gps_directions(latitude, longitude):
        geolocator = Nominatim(user_agent="MED10-MASTER-THESIS-PROJECT")
        time.sleep(1)
        location = geolocator.reverse([latitude, longitude], exactly_one=True)
        return location.address if location else "No address found."



def download_faces(split_panos):
    with Pool(num_processes) as pool:
        pool.map(download_func_with_downloader, split_panos)
        pool.close()
        pool.join()

def download_func_with_downloader(args):
    panorama, downloader = args
    # Define the url, tile_xpos, and tile_ypos
    url = "https://www.google.com"
    tile_xpos = 69144
    tile_ypos = 40119
    return downloader.download_panorama_face(panorama, url, tile_xpos, tile_ypos)


# Exmaple usage
if __name__ == "__main__":
    downloader = LookAroundImageDownloaderFromTile(debug=False)
    panos = downloader.get_coverage_tile(69144, 40119)

    print(f'Got {len(downloader.panos)} panoramas')

    timer = time.time()

    # To speed up the process we can first split the list of panoramas into 4 parts and then download them in parallel
    split_panos = [panos[i::4] for i in range(4)]  # Split the list into 4 parts

    # Prints the length of each split list
    for i in range(4):
        print(f"Length of split_panos[{i}] = {len(split_panos[i])}")

    # Number of processes you want to run concurrently
    num_processes = 4
    counter = 0

    # Use a regular function instead of a lambda
    with Pool(num_processes) as pool:
        flat_panos = [item for sublist in split_panos for item in sublist]
        start_time = time.time()  # Start the timer
        pool.map(download_func_with_downloader, [(panorama, downloader) for panorama in flat_panos])

        end_time = time.time()  # End the timer
        downloader.save_data()

    print(f"Total time for downloading: {end_time - start_time} seconds")
