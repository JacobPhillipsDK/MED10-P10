import os


def main():
    counter = 0
    for i in os.listdir("TestFolder/jpg_cut"):
        for j in os.listdir(f"TestFolder/jpg_cut/{i}"):
            counter += 1

    print(f"Total images : {counter}")
    print("#################################################")

    list11 = ['69144_40119', '69144_40120', '69144_40121', '69144_40127', '69145_40119', '69145_40120', '69146_40120',
              '69146_40121', '69146_40127', '69147_40120', '69147_40121', '69148_40121', '69148_40125', '69149_40121',
              '69149_40123', '69149_40124', '69149_40125', '69151_40124', '69151_40125', '69151_40126', '69151_40128',
              '69152_40123', '69152_40126']
    print(f"len of Jacob_list: {len(list11)}")



    list22 = ['69144_40122', '69144_40123', '69144_40124', '69144_40125', '69144_40126', '69145_40121', '69145_40122',
              '69145_40123', '69145_40124', '69145_40127', '69145_40128', '69146_40119', '69146_40122', '69146_40123',
              '69146_40124', '69146_40125', '69146_40126', '69146_40128', '69147_40119', '69147_40123', '69147_40124',
              '69147_40125', '69147_40126', '69147_40128', '69148_40119', '69148_40120', '69148_40122', '69148_40123',
              '69148_40124', '69148_40125', '69148_40126', '69148_40127', '69148_40128', '69149_40122', '69149_40126',
              '69149_40127', '69149_40128', '69150_40122', '69150_40123', '69150_40124', '69150_40125', '69150_40126',
              '69150_40128', '69151_40122', '69151_40123', '69151_40125', '69151_40127', '69152_40122', '69152_40123',
              '69152_40124', '69152_40125', '69152_40127', '69152_40128']

    print(f"len of Calvin_list: {len(list22)}")

    for x in list22:
        print(f"{x} : len  = {len(os.listdir(f'TestFolder/jpg_cut/{x}'))}")

    combined_list = list11 + list22

    print(f"Combined {len(list11)} +  {len(list22)} = {len(list11) + len(list22)}")

    print("#################################################")

    # Convert the lists to sets
    set11 = set(list11)
    set22 = set(list22)

    # Find the intersection (common elements) between the two sets
    duplicates = set11.intersection(set22)

    print(f"Duplicate elements between list11 and list22: {duplicates} : len {len(duplicates)}")

    print("#################")

    dup_counter = 0
    for i in duplicates:
        internal_counter = 0
        for j in os.listdir(f"TestFolder/jpg_cut/{i}"):
            dup_counter += 1
            internal_counter += 1
        print(f"Total images in {i}: {internal_counter}")

    print(f"Total images in found dup folders: {dup_counter}")

    print("#################################################")

    folder_list = os.listdir(f"TestFolder/jpg_cut")

    # we remove the duped folders from the folder_list

    print("we remove the duped folders from the folder_list")
    # Convert the lists to sets for efficient comparison
    combined_set = set(combined_list)
    folder_set = set(folder_list)

    print("#################")

    combined_set_counter = 0
    for i in combined_set:
        for j in os.listdir(f"TestFolder/jpg_cut/{i}"):
            combined_set_counter += 1

    print(f"Combined set counter: {combined_set_counter}")

    print("#################")


    print("Length of combined_set:", len(combined_set))
    print("Length of folder_list:", len(folder_set))

    print(f"There is {len(folder_set) - len(combined_set)} missing folders in the folder_list")

    missing_folders = folder_set - combined_set

    print(f"Missing folders: {missing_folders}")

    print("#################################################")

    print("We count the images in the missing folders")


    missing_counter = 0

    for i in missing_folders:
        _counter = 0
        for j in os.listdir(f"TestFolder/jpg_cut/{i}"):
            _counter += 1
        print(f"Total images in {i}: {_counter}")
        missing_counter += _counter

    print(f"Total images in the missing folders: {missing_counter}")



    print("#################################################")
    print(" check if the missing items multipled with the combined set equal the length of the folder list")
    print(f"Combined set counter: {combined_set_counter}")
    print(f"Missing counter: {missing_counter}")
    print(f"Combined set counter + Missing counter = {combined_set_counter + missing_counter}")
    print(f"Total images : {counter}")





    list11_counter = sum(len(os.listdir(f"TestFolder/jpg_cut/{i}")) for i in list11)
    print(f"Total images in list11: {list11_counter}")

    list22_counter = sum(len(os.listdir(f"TestFolder/jpg_cut/{i}")) for i in list22)
    print(f"Total images in list22: {list22_counter}")

    print(f"diff: {list22_counter - list11_counter}")

    print(list22_counter - (list11_counter + missing_counter))


if __name__ == "__main__":
    main()
