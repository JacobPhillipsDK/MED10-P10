import os
import time
from PIL import Image


from streetlevel import streetview

pano = streetview.find_panorama(57.048028567059944, 9.928551711992268)
streetview.download_panorama(pano, f"{pano.id}.jpg", zoom=2)

def crop_image(image_path, output_folder):
    # Open the image
    img = Image.open(image_path)

    # Get image dimensions
    width, height = img.size

    # Calculate the new height for a 4:1 ratio
    new_height = width // 4

    # Calculate the cropping dimensions
    upper_crop = (height - new_height) // 2
    lower_crop = height - upper_crop

    # Crop the image
    img_cropped = img.crop((0, upper_crop, width, lower_crop))

    # Split the cropped image into four equal parts horizontally
    split_width = width // 4
    for i in range(4):
        left = i * split_width
        right = (i + 1) * split_width
        img_part = img_cropped.crop((left, 0, right, new_height))
        img_part.save(f"{output_folder}/image_part_{i}.jpg")

# Example usage
input_image_path = f'{pano.id}.jpg'
output_folder = "output_images"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Measure the time taken
start_time = time.time()

crop_image(input_image_path, output_folder)

end_time = time.time()
elapsed_time = end_time - start_time
print("Time taken:", elapsed_time, "seconds")