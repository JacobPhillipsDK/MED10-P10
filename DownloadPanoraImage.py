from streetlevel import lookaround



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

class LookAroundImageDownloaderFromTile:
    def __init__(self, tile_x, tile_y, zoom=0):
        self.auth = lookaround.Authenticator()
        self.zoom = zoom  # zoom (int) – The zoom level. 0 is highest, 7 is lowest. | Lowest means less detailed
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)

    @staticmethod
    def get_coverage_tile(x, y):
        return lookaround.get_coverage_tile(x, y)

    def image_metaData(self, panos) -> None:

        panos_ID = str(panos[0].id)
        panos_build_ID = str(panos[0].build_id)
        panos_lat = str(panos[0].lat)
        panos_lon = str(panos[0].lon)
        panos_date = str(panos[0].date)

        print(f"""
        Got {len(panos)} panoramas. Here's one of them:
        ID: {panos[0].id}\t\tBuild ID: {panos[0].build_id}
        Latitude: {panos[0].lat}\tLongitude: {panos[0].lon}
        Capture date: {panos[0].date}
        """)

    def download_panorama_face(self, panorama, file_path, zoom=None) -> None:
        if zoom is None:
            zoom = self.zoom
        for face in range(0, 4):
            lookaround.download_panorama_face(panorama, file_path, face, zoom, self.auth)


if __name__ == "__main__":
    # auth = lookaround.Authenticator()
    # zoom = 2
    # for face in range(0, 1):
    #     lookaround.download_panorama_face(panos[0], f"TestFolder/{panos[0].id}_{face}_{zoom}.heic",
    #                                       face, zoom, auth)

    downloader = LookAroundImageDownloaderFromTile(69150, 40123)
    downloader.image_metaData(downloader.panos)

