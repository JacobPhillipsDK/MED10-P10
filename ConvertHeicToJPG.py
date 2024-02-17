from PIL import Image
from pillow_heif import register_heif_opener
import os


class HeicToJpgConverter:
    def __init__(self):
        register_heif_opener()
        self.folder_structure()
        self.folder_name = ""

    def folder_structure(self, folder_name='TestFolder'):
        # Create a folder structure where it will store the converted images
        # first we check if the correct folder is already created from the scripts path
        # if not we create the folder structure
        self.folder_name = f'{os.path.join(os.path.dirname(__file__), folder_name)}'

        if not os.path.exists(f'{folder_name}'):
            try:
                os.makedirs(f'{folder_name}')
                print(f'Folder created successfully with the name {folder_name}')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            print(f'Folder already exists with the name {folder_name}')

        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{folder_name}/heic'):
            try:
                os.makedirs(f'{folder_name}/heic')
                print(f'Folder created successfully with the name {folder_name}/heic')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")
        else:
            print(f'Folder already exists with the name {folder_name}/heic')

        # Create a folder structure where it will store the converted images
        if not os.path.exists(f'{folder_name}/jpg'):
            try:
                os.makedirs(f'{folder_name}/jpg')
                print(f'Folder created successfully with the name {folder_name}/jpg')
            except Exception as e:
                print(f"An error occurred while creating the folder: {e}")

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
    converter.folder_structure()
