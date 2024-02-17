from PIL import Image
from pillow_heif import register_heif_opener
import os
from FolderStructure import FolderStructure


class HeicToJpgConverter(FolderStructure):
    def __init__(self):
        super().__init__()
        register_heif_opener()


        # Create a folder structure where it will store the converted images
        _FolderStructure = FolderStructure()
        _FolderStructure.create_folder_structure()
        _FolderStructure.create_heic_jpg_folders()

    def convert_heic_to_jpg(self, heic_file_path, jpg_file_path=None):

        if jpg_file_path is None:
            jpg_file_path = self.folder_name

        try:
            image = Image.open(heic_file_path)
            image.save(jpg_file_path)
            print(f"Converted {heic_file_path} to {jpg_file_path}")
        except Exception as e:
            print(f"An error occurred while converting {heic_file_path} to {jpg_file_path}: {e}")

    def convert_multiple_heic_to_jpg(self, heic_folder_path, jpg_folder_path=None):

        if jpg_folder_path is None:
            jpg_folder_path = self.folder_name

        for file in os.listdir(heic_folder_path):
            if file.endswith(".heic"):
                heic_file_path = os.path.join(heic_folder_path, file)
                jpg_file_path = os.path.join(jpg_folder_path, file.replace(".heic", ".jpg"))
                self.convert_heic_to_jpg(heic_file_path, jpg_file_path)


if __name__ == "__main__":
    converter = HeicToJpgConverter()
