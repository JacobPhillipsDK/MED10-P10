import json
import os
import re
from urllib.parse import unquote
import shutil

label_names = {
    "0": "Street art",
    "1": "Modern architecture",
    "2": "Historic buildings",
    "3": "Statues/Sculptures",
    "4": "Bridge",
    "5": "Ships/Boats",
    "6": "Seawater",
    "7": "Dock cleat",
    "8": "Dock",
    "9": "Park",
    "10": "Trees",
    "11": "Pond/River",
    "12": "Bush",
    "13": "Sport fields",
    "14": "Stadium",
    "15": "Playground/outdoor workout",
    "16": "Bar/Pub",
    "17": "Supermarket",
    "18": "Mall",
    "19": "Stores",
    "20": "Restaurants/Cafe",
    "21": "Pedestrian street",
    "22": "Hotel",
    "24": "Fence/Walls/hedges",
    "23": "Apartment building",
    "25": "Garden",
    "26": "House",
    "27": "Bus stop",
    "28": "Parking area",
    "29": "Urban greening",
    "30": "Transport hub",
    "31": "Hospital/police stations"
}


def extract_folder_name(data):
    data_field = data.get("data", {})
    image_path = data_field.get("image", "")

    # Decode the URL-encoded path
    decoded_path = unquote(image_path)

    # Updated pattern to match different folder name formats
    patterns = [
        r"Pictures/jpg_cut/(\d+_\d+)/\d+_\d+\.jpg",
        r"Pictures\\jpg_cut\\(\d+_\d+)\\",
        r"Pictures%5Cjpg_cut%5C(\d+_\d+)%5C"
    ]

    for pattern in patterns:
        match = re.search(pattern, decoded_path)
        if match:
            folder_name = match.group(1)
            return folder_name

    return None


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def total_annotations(data):
    total_annotations = 0

    # Iterate through each task
    for task in data:
        # Count the number of annotations for the current task
        task_annotations = len(task['annotations'])
        total_annotations += task_annotations

    print(f"Total number of annotations: {total_annotations}")

    label_counts = {}

    # Iterate through each task
    for task in data:
        # Iterate through each annotation in the task
        for annotation in task['annotations']:
            # Check if the annotation has a result
            if annotation['result']:
                # Get the choices from the result
                choices = annotation['result'][0]['value']['choices']
                # Iterate through each choice (label number)
                for choice in choices:
                    # Get the label name from the dictionary
                    label_name = label_names.get(choice, choice)
                    # Update the count for the current label
                    label_counts[(choice, label_name)] = label_counts.get((choice, label_name), 0) + 1

    # Print the label counts
    for (label_number, label_name), count in label_counts.items():
        print(f"Label number {label_number} ({label_name}) : appeared {count} times.")


# We want to change the names of the json file to
# the names of the folder name and the number total images

def copy_rename():
    folder_path = os.listdir("CSV und JSON  - Jacob")

    # filter the folder_path for files ending with .json
    folder_path = [file for file in folder_path if file.endswith(".json")]

    print("folder", len(folder_path))

    for i in [file for file in folder_path if file.endswith(".json")]:

        # Load the JSON data
        path = f"CSV und JSON  - Jacob/{i}"

        print("path", path)

        with open(path, 'r') as file:
            data = json.load(file)

        # Get the first task
        task = data[0]
        folder_name = extract_folder_name(task)

        total_annotations = 0

        # Iterate through each task
        for task in data:
            # Count the number of annotations for the current task
            task_annotations = len(task['annotations'])
            total_annotations += task_annotations

        # copy the file to the new name
        new_name = f"{folder_name}_{total_annotations}.json"

        # copy the file and move to different folder

        shutil.copy(f"CSV und JSON  - Jacob/{i}", f"json_folder/{new_name}")


def count_choice_occurrences(data, choices):
    choice_counts = {}
    for choice in choices:
        choice_counts[choice] = 0

    for task in data:
        annotations = task['annotations']
        for annotation in annotations:
            if annotation['result']:
                annotation_choices = annotation['result'][0]['value']['choices']
                for choice in choices:
                    if choice in annotation_choices:
                        choice_counts[choice] += 1

    for choice, count in choice_counts.items():
        label_name = label_names.get(choice, choice)
        print(f"Choice '{choice}' ({label_name}) appeared in {count} images.")

    return choice_counts


def remove_mistakes(file_path):
    data = load_json_file(file_path)

    print("#############################################################################################################")
    print(f'Name of the file: {file_path}')

    total_annotations(data)

    # specific find the instances where we have both House and Fence/Walls/hedges in the same image
    instances = []
    images_with_choice_26 = []
    for task in data:
        annotations = task['annotations']
        choices = [annotation['result'][0]['value']['choices'] for annotation in annotations if annotation['result']]
        flattened_choices = [choice for choices_list in choices for choice in choices_list]
        if "26" in flattened_choices and "24" in flattened_choices:
            instances.append(task)
        if "26" in flattened_choices:
            images_with_choice_26.append(task['data']['image'])

    print(f"Number of instances where both 'House' and 'Fence/Walls/hedges' are present: {len(instances)}")

    ##  filter the URL naming syntax
    # ['/data/local-files/?d=Pictures%5Cjpg_cut%5C69144_40128%5C11006107550227150150_0.jpg
    # becomes
    # 69144_40128_11006107550227150150_0.jpg

    images_with_choice_26 = [re.search(r"\d+_\d+_\d+\.jpg", image).group() for image in images_with_choice_26 if re.search(r"\d+_\d+_\d+\.jpg", image) is not None]

    print("Images with choice 26:")
    print(images_with_choice_26)

    print("#############################################################################################################")


if __name__ == "__main__":
    # for i in os.listdir("json_folder"):
    #     remove_mistakes(f"json_folder/{i}")

    remove_mistakes("json_folder/69144_40128_904.json")
