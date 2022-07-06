import os, glob, shutil, random

images_folder = "./images/"
labels_folder = "./labels/"

folders = ["train", "val"]

for folder in folders:
    os.makedirs(images_folder+folder, exist_ok=True)
    os.makedirs(labels_folder+folder, exist_ok=True)

image_list = glob.glob(images_folder+"*.jpg") 
random.shuffle(image_list)

for i, image_file in enumerate(image_list):
    print(i, image_file)
    image_file_name = os.path.basename(image_file)
    label_file_name = os.path.basename(image_file)[:-4] + ".txt"
    label_file = labels_folder + label_file_name
    print(label_file_name)
    try:
        if i < int(len(image_list)*0.8):
            shutil.copy(image_file, images_folder + folders[0] + "/" + image_file_name)
            shutil.copy(label_file, labels_folder + folders[0] + "/" + label_file_name)
        else:
            shutil.copy(image_file, images_folder + folders[1] + "/" + image_file_name)
            shutil.copy(label_file, labels_folder + folders[1] + "/" + label_file_name)
    except FileNotFoundError:
        print("File not found")

    #shutil.copy()