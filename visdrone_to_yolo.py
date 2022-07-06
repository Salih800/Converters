import os, glob
import shutil

from PIL import Image

pics_path = "C:/Users/Salih/Downloads/VisDrone2019-DET-val/images/"
labels_path = "C:/Users/Salih/Downloads/VisDrone2019-DET-val/annotations/*"

label_list = ["left", "top", "width", "height", "confidence", "category", "truncation", "occlusion"]
i = 0

yolo_format = ["class_id", "x", "y", "w", "h"]

my_labels_path = "C:/Users/Salih/Downloads/VisDrone2019-DET-val/labels/"
if os.path.isdir(my_labels_path):
    shutil.rmtree(my_labels_path)
os.mkdir(my_labels_path)

label_file_list = glob.glob(labels_path)
print(f"Total {len(label_file_list)} files")
for label_file in label_file_list:
    yolo_dict_list = []
    with open(label_file, "r") as labels:
        img_name = os.path.basename(label_file)[:-4]
        img = Image.open(pics_path + img_name + ".jpg")
        # print(img.size)
        # print(label_file)
        # print(img_name)
        label_lines = labels.read().split()
        # print(label_lines)
    for label in label_lines:
        # left, top, width, height, confidence, category, truncation, occlusion = label.split(",")
        label_split = label.split(",")
        label_dict = {}
        yolo_dict = {}
        yolo_list = []
        for j, label_info in enumerate(label_list):
            label_dict[label_info] = int(label_split[j])
        # print(label_dict)
        if label_dict["category"] in [1, 4, 5, 6, 9, 10]:
            if label_dict["category"] == 1:
                yolo_list = 0, (label_dict["left"] + label_dict["width"] / 2) / img.width, \
                            (label_dict["top"] + label_dict["height"] / 2) / img.height, \
                            (label_dict["width"] / img.width), (label_dict["height"] / img.height)
            else:
                yolo_list = 1, (label_dict["left"] + label_dict["width"] / 2) / img.width, \
                            (label_dict["top"] + label_dict["height"] / 2) / img.height, \
                            (label_dict["width"] / img.width), (label_dict["height"] / img.height)

            for k, label_info in enumerate(yolo_format):
                # if label_info == "class_id":
                #     yolo_dict[label_info] = int(yolo_list[k])
                yolo_dict[label_info] = yolo_list[k]
            # print(yolo_dict)
            # print(*yolo_dict.values())
            yolo_label = f"{yolo_dict['class_id']} {yolo_dict['x']} {yolo_dict['y']} {yolo_dict['w']} {yolo_dict['h']}"
            if yolo_label not in yolo_dict_list:
                yolo_dict_list.append(yolo_label)
            else:
                print(f"same label in it: {label_file}: {label_dict}")

    with open(my_labels_path + img_name + ".txt", "w") as my_label_file:
        my_label_file.write("\n".join(yolo_dict_list))
        # my_label_file.write(*yolo_dict_list)
        # my_label_file.write("\n")
        # print(*yolo_dict_list)
    # i += 1
    # if i == 1:
    #     break
