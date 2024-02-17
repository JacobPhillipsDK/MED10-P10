from streetlevel import lookaround
from CreateDataSet import CreateImageMetaData
from geopy.geocoders import Nominatim


# panos = lookaround.get_coverage_tile(69150, 40123)

# Print the 100 first panoramas ID
# for i in range(1):
#     print(panos[i].id)
#     auth = lookaround.Authenticator()
#     zoom = 0
#     for face in range(0, 6):
#         lookaround.download_panorama_face(panos[i], f"TestFolder/{panos[i].id}_{face}_{zoom}.heic",
#                                           face, zoom, auth)

# print(f"""
# Got {len(panos)} panoramas. Here's one of them:
# ID: {panos[0].id}\t\tBuild ID: {panos[0].build_id}
# Latitude: {panos[0].lat}\tLongitude: {panos[0].lon}
# Capture date: {panos[0].date}
# """)
#

class LookAroundImageDownloaderFromTile(CreateImageMetaData):
    def __init__(self, tile_x, tile_y, zoom=0):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.zoom = zoom  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)

    @staticmethod
    def get_coverage_tile(x, y):
        return lookaround.get_coverage_tile(x, y)

    def image_metaData(self) -> tuple:

        panos_ID = str(self.panos[0].id)
        panos_build_ID = str(self.panos[0].build_id)
        panos_lat = str(self.panos[0].lat)
        panos_lon = str(self.panos[0].lon)
        panos_date = str(self.panos[0].date)

        address = self.get_gps_directions(panos_lat, panos_lon)

        print(f"""
        Got {len(self.panos)} panoramas. Here's one of them:
        ID: {self.panos[0].id}\t\tBuild ID: {self.panos[0].build_id}
        Latitude: {self.panos[0].lat}\tLongitude: {self.panos[0].lon}
        Capture date: {self.panos[0].date}\tAddress: {address}
        """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, address

    def download_panorama_face(self, panorama, zoom=None) -> None:
        if zoom is None:
            zoom = self.zoom
        for face in range(0, 4):
            lookaround.download_panorama_face(pano=panorama, path=self.jpg_path, face=face, zoom=zoom, auth=self.auth)

    @staticmethod
    def get_gps_directions(latitude, longitude):
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse([latitude, longitude], exactly_one=True)
        return location.address if location else "No address found."


# Exmaple usage
if __name__ == "__main__":
    # auth = lookaround.Authenticator()
    # zoom = 2
    # for face in range(0, 1):
    #     lookaround.download_panorama_face(panos[0], f"TestFolder/{panos[0].id}_{face}_{zoom}.heic",
    #                                       face, zoom, auth)

    downloader = LookAroundImageDownloaderFromTile(69150, 40123)
    downloader.download_panorama_face(downloader.panos[0])
