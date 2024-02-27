import pandas as pd
from FolderStructure import FolderStructure
from streetlevel import lookaround
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

        self.columns = ['Image Name', 'ID', 'Build ID', 'Latitude', 'Longitude', 'Capture date', 'URL']
        self.df = pd.DataFrame(columns=self.columns)

        # Create a folder structure where it will store the converted images
        self._FolderStructure = FolderStructure()
        self._FolderStructure.create_folder_structure()
        self.folder_to_save_path = self._FolderStructure.folder_name

    def append_image_data(self, image_name, panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, URL, tile_xpos,
                          tile_ypos, address, face_value) -> None:
        """Append the data to the dataframe"""
        new_data = {
            'Image Name': image_name,
            'ID': panos_ID,
            'Face': face_value,
            'Build ID': panos_build_ID,
            'Latitude': panos_lat,
            'Longitude': panos_lon,
            'Capture date': panos_date,
            'URL': URL,
            'Tile X': tile_xpos,
            'Tile Y': tile_ypos,
            'Street Address': address
        }
        new_df = pd.DataFrame([new_data])  # Create a new DataFrame with the new data
        self.df = pd.concat([self.df, new_df], ignore_index=True)  # Concatenate the new DataFrame to the existing one
        # print(f"Appending data for image {image_name}")
        # print(self.df)  # print the DataFrame to check if the data is being appended
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

        # print(f"""
        #           Got {len(self.panos)} panoramas. Here's one of them:
        #           ID: {panorama.id}\t\tBuild ID: {panorama.build_id}
        #           Latitude: {panorama.lat}\tLongitude: {panorama.lon}
        #           Capture date: {panorama.date}
        #           """)

        return panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date

    def match_image_data_to_image(self,  tile_xpos, tile_ypos, URL="URL"):
        # from get_coverage_tile we get the panorama data and we can match it to the image that we have downloaded to then create the metadata csv file

        # first we need to get the image name from the image that we have downloaded
        # then we need to get the panorama data from the get_coverage_tile

        images_by_tile = self.get_coverage_tile(tile_xpos, tile_xpos)

        downloaded_images = os.listdir(f"TestFolder/heic/{tile_xpos}_{tile_ypos}")
        # Extracting the first ID from each filename
        seperated_downloaded_images = [filename.split('_')[0] for filename in downloaded_images]

        duplicates_removed = list(set(seperated_downloaded_images))

        for i in range(len(images_by_tile)):

            for k in range(len(duplicates_removed)):

                if int(images_by_tile[i].id) == int(duplicates_removed[k]):

                    for j in range(0, 4):
                        # get image data
                        panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date = self.image_metaData(
                            images_by_tile[i])

                        # now we can check if both panos_ID and panos_build_ID are in the downloaded images
                        # if they are we can append the data to the datafram
                        self.append_image_data(image_name=f'{duplicates_removed[i]}_{j}.heic', panos_ID=panos_ID,
                                               panos_build_ID=panos_build_ID,
                                               panos_lat=panos_lat, panos_lon=panos_lon, panos_date=panos_date, URL=URL,
                                               tile_xpos=tile_xpos, tile_ypos=tile_ypos,
                                               address=self.get_gps_directions(latitude=panos_lat, longitude=panos_lon),
                                               face_value=j)

        self.save_to_csv()

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

    # MetaData.append_image_data(image_name="image_name", panos_ID="panos_ID", panos_build_ID="panos_build_ID",
    #                            panos_lat="panos_lat", panos_lon="panos_lon", panos_date="panos_date", URL="URL",
    #                            tile_xpos="tile_xpos", tile_ypos="tile_ypos", address="address", face_value="face_value")
    # MetaData.save_to_csv()
    # print(MetaData.df)
    MetaData.match_image_data_to_image()
