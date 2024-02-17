from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import datetime
from fractions import Fraction

import piexif

def add_gps_metadata(image_path, latitude, longitude, original_time):
    # Open the image
    image = Image.open(image_path)

    # Convert the GPS coordinates and altitude to the format that piexif expects
    lat_deg = to_deg(latitude, ["S", "N"])
    lng_deg = to_deg(longitude, ["W", "E"])

    exiv_lat = (change_to_rational(lat_deg[0]), change_to_rational(lat_deg[1]), change_to_rational(lat_deg[2]))
    exiv_lng = (change_to_rational(lng_deg[0]), change_to_rational(lng_deg[1]), change_to_rational(lng_deg[2]))

    # Create new EXIF data
    gps_ifd = {
        piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1,
        piexif.GPSIFD.GPSAltitude: change_to_rational(0),  # Assuming altitude is 0
        piexif.GPSIFD.GPSLatitudeRef: lat_deg[3],
        piexif.GPSIFD.GPSLatitude: exiv_lat,
        piexif.GPSIFD.GPSLongitudeRef: lng_deg[3],
        piexif.GPSIFD.GPSLongitude: exiv_lng,
    }

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)

    # Save the image with the updated EXIF data
    piexif.insert(exif_bytes, image_path)

    print("GPS Metadata added successfully!")
# Example usage
image_path = "TestFolder/jpg/11006107550211883488_0_0.jpg"
latitude = 37.7749  # Replace with actual latitude
longitude = -122.4194  # Replace with actual longitude
original_time = datetime.datetime(2024, 2, 14, 12, 0, 0)  # Replace with actual time

add_gps_metadata(image_path, latitude, longitude, original_time)
