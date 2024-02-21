import pandas as pd
from FolderStructure import FolderStructure


class CreateImageMetaData(FolderStructure):
    def __init__(self, filename=None):
        super().__init__()
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
        """Append the data the dataframe"""
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
        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        print(f"Appending data for image {image_name}")
        print(self.df)  # print the DataFrame to check if the data is being appended
        return None

    def save_to_csv(self) -> None:
        """Save the dataframe to a csv file"""
        self.df.to_csv(f'{self.folder_to_save_path}/{self.filename}', index=False)

        print("Saving data to CSV")
        print(self.df)  # print the DataFrame to check if it contains the expected data
        return None


if __name__ == "__main__":
    MetaData = CreateImageMetaData()
    MetaData.append_image_data(image_name="image_name", panos_ID="panos_ID", panos_build_ID="panos_build_ID",
                               panos_lat="panos_lat", panos_lon="panos_lon", panos_date="panos_date", URL="URL",
                               tile_xpos="tile_xpos", tile_ypos="tile_ypos", address="address", face_value="face_value")
    MetaData.save_to_csv()
    print(MetaData.df)
