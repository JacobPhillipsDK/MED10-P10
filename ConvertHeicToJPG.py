from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()
image = Image.open('TestFolder/11006107550211883488_0_7.heic')
image.save('TestFolder/11006107550211883488_0_7.jpg')