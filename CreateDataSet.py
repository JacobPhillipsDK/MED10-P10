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
        self.df = self.create_PandaDataFrame()

        # Create a folder structure where it will store the converted images
        self._FolderStructure = FolderStructure()
        self._FolderStructure.create_folder_structure()
        self.folder_to_save_path = self._FolderStructure.folder_name


    def create_PandaDataFrame(self, ) -> pd.DataFrame:
        """Creates a panda dataframe with the columns specified in the class variable columns"""
        df = pd.DataFrame(columns=self.columns)
        return df

    def append_image_data(self, image_name, panos_ID, panos_build_ID, panos_lat, panos_lon, panos_date, URL, tile_xpos, tile_ypos, address) -> None:
        """Append the data the dataframe"""
        new_data = {
            'Image Name': image_name,
            'ID': panos_ID,
            'Build ID': panos_build_ID,
            'Latitude': panos_lat,
            'Longitude': panos_lon,
            'Capture date': panos_date,
            'URL': URL,
            'Tile X': tile_xpos,
            'Tile Y': tile_ypos,
            'Street Address': address
        }
        self.df.append(new_data, index=False)
        return None


    def save_to_csv(self) -> None:
        """Save the dataframe to a csv file"""
        self.df.to_csv(f'{self.folder_to_save_path}/{self.filename}', index=False)
        return None

if __name__ == "__main__":
    pass
