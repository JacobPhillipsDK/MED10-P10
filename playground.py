import pandas as pd

from streetlevel import lookaround


# 57.043006775157295, 9.934045093901023
# tile coordinates: 69152_40126


def main():
    headers = ['Image Name', 'ID', 'Face', 'Build ID', 'Latitude', 'Longitude', 'Capture date', 'image_url',
               'Has Blurs', 'tile_URL', 'Coverage Type', 'Image tile', 'Street Address']

    # loads the csv file into a pandas DataFrame
    df = pd.read_csv('csv files/ImageMetaDataSet.csv')

    # Drop duplicates based on the 'ID' column, keeping the first occurrence
    df_deduplicated = df.drop_duplicates('ID', keep='first')

    print(len(df), len(df) / 4)
    print(len(df_deduplicated))

    # Save the deduplicated DataFrame to a new CSV file
    df_deduplicated.to_csv('deduplicated_data.csv', index=False)


if __name__ == "__main__":
    main()
