import pandas as pd
from FolderStructure import FolderStructure
from streetlevel import lookaround
import streetlevel
from geopy.geocoders import Nominatim
import time
from random import choice
from random import randint
import os


class CreateImageMetaData(FolderStructure):
    def __init__(self, filename=None):
        super().__init__()
        self.auth = lookaround.Authenticator()
        self.panos = None

        if filename is not None:
            self.filename = filename
        else:
            self.filename = "ImageMetaData.csv"

        self.columns = ['Image Name', 'ID', 'Face', 'Build ID', 'Latitude','Longitude', 'Capture date', 'image_url',
                        'Has Blurs', 'tile_URL', 'Coverage Type', 'Image tile', 'Street Address']
        self.df = pd.DataFrame(columns=self.columns)

        # Create a folder structure where it will store the converted images
        self._FolderStructure = FolderStructure()
        self._FolderStructure.create_folder_structure()
        self.folder_to_save_path = self._FolderStructure.folder_name


    def append_image_data(self, image_name, panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, image_url,
                          tile_URL, tile_coordinate, address, face_value, has_blur, coverage_type) -> None:
        """Append the data to the dataframe"""
        new_data = {
            'Image Name': image_name,
            'ID': panos_ID,
            'Face': face_value,
            'Build ID': panos_build_ID,
            'Latitude': panos_lat,
            'Longitude': panos_lon,
            'Capture date': panos_date,
            'image_url': image_url,
            'Has Blurs': has_blur,
            'tile_URL': tile_URL,
            'Coverage Type': coverage_type,  # 'CAR' or 'BACKPACK
            'Image tile': tile_coordinate,
            'Street Address': address,
        }
        new_df = pd.DataFrame([new_data])  # Create a new DataFrame with the new data
        self.df = pd.concat([self.df, new_df], ignore_index=True)  # Concatenate the new DataFrame to the existing one

        print(f"Appending data for image {image_name}")
        print(self.df)  # print the DataFrame to check if the data is being appended
        return None


    def get_coverage_tile(self, tile_x, tile_y):
        self.panos = lookaround.get_coverage_tile(tile_x, tile_y)
        return self.panos


    def image_metaData(self, panorama) -> tuple:
        panos_ID = str(panorama.id)
        panos_build_ID = str(panorama.build_id)
        panos_lat = str(panorama.lat)
        panos_lon = str(panorama.lon)
        panos_date = str(panorama.date)
        panos_permalink = str(panorama.permalink())  # Add parentheses here
        panos_coverage_type = str(panorama.coverage_type)
        panos_has_blurs = str(panorama.has_blurs)
        panos_tile = str(panorama.tile)

        # print(f"""
        #           Got {len(self.panos)} panoramas. Here's one of them:
        #           ID: {panorama.id}\t\tBuild ID: {panorama.build_id}
        #           Latitude: {panorama.lat}\tLongitude: {panorama.lon}
        #           Capture date: {panorama.date}\tPermalink: {panos_permalink}\tCoverage Type: {panorama.coverage_type}\tHas Blurs: {panorama.has_blurs}
        #           \t Tile: {panorama.tile}
        #
        #
        #           """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, panos_permalink, panos_coverage_type, panos_has_blurs, panos_tile


    def match_image_data_to_image(self):
        # from get_coverage_tile we get the panorama data and we can match
        # it to the image that we have downloaded to then create the metadata csv file

        # first we need to get the image name from the image that we have downloaded
        # then we need to get the panorama data from the get_coverage_tile

        counter = 0

        for i in os.listdir(self.heic_path):

            tile_xpos = int(i.split("_")[0])
            tile_ypos = int(i.split("_")[1])

            images_by_tile = self.get_coverage_tile(tile_xpos, tile_ypos)

            duplicates_removed = list(set([filename.split('_')[0] for filename in os.listdir(f"{self.heic_path}/{i}")]))

            url = f"https://tile.openstreetmap.org/17/{tile_xpos}/{tile_ypos}.png"

            for k in range(len(duplicates_removed)):

                if int(images_by_tile[k].id) == int(duplicates_removed[k]):

                    if counter > 1:
                        break

                    for j in range(0, 4):
                        # get image data
                        panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, panos_permalink, panos_coverage_type, panos_has_blurs, panos_tile = self.image_metaData(
                            images_by_tile[k])

                        # check if panos tile is the same as the downloaded one
                        # Tile: (69144, 40119, 17)
                        # seperate so we get the x and y coordinates

                        panos_tile_x = int(panos_tile.split(",")[0].replace("(", ""))
                        panos_tile_y = int(panos_tile.split(",")[1].replace(")", ""))

                        # we want to check if they match
                        if panos_tile_x == tile_xpos and panos_tile_y == tile_ypos:
                            print(f"Tile: {panos_tile} is the same as the downloaded tile: {tile_xpos}_{tile_ypos}")

                            # now we can check if both panos_ID and panos_build_ID are in the downloaded images

                            self.append_image_data(image_name=f'{duplicates_removed[k]}_{j}', panos_ID=panos_ID,
                                                   panos_build_ID=panos_build_ID, panos_lat=panos_lat,
                                                   panos_lon=panos_lon, panos_date=panos_date,
                                                   image_url=panos_permalink, tile_URL=url,
                                                   tile_coordinate=panos_tile,
                                                   address=self.get_gps_directions(panos_lat, panos_lon), face_value=j,
                                                   has_blur=panos_has_blurs, coverage_type=panos_coverage_type)

                    counter += 1


    @staticmethod
    def get_gps_directions(latitude, longitude):
        # random list of user_agents to avoid getting blocked
        user_agents = ["SemesterAgentOne", "ProjectExplorerAgent", "MED10-MASTER-THESIS-PROJECT",
                       "CodeCraftNavigator", "QuantumSemesterSurfer", "ByteBusterNavigator", "PolyglotSemesterSailor",
                       "MetaCodeAdventurer", "SyntaxSeekerExplorer", "AlgorithmicVoyagerAgent", "DataDrivenNavigator",
                       "QuantumBytePioneer"]

        # pick a random user_agent
        geolocator = Nominatim(user_agent=choice(user_agents))
        time.sleep(randint(1, 5))  # sleep for a random time between 1 and 5 seconds so we don't get blocked
        location = geolocator.reverse([latitude, longitude], exactly_one=True)
        return location.address if location else "No address found."


    def save_to_csv(self) -> None:
        """Save the dataframe to a csv file"""
        self.df.to_csv(f'{self.folder_to_save_path}/{self.filename}', index=False)

        print("Saving data to CSV")
        # prints the row and column count of the dataframe
        print(self.df.shape)
        return None


if __name__ == "__main__":
    MetaData = CreateImageMetaData()
    MetaData.match_image_data_to_image()
    MetaData.save_to_csv()
