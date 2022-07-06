import sys
import xml.etree.ElementTree as ET
import glob
import os
import json
import shutil


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width heigth
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


classes = ["pedestrian", "vehicle", "uap", "uap_not", "uai", "uai_not"]
input_dir = "C:/Users/Salih/Desktop/Teknofest UYZ 2021 Etiketli Veriler/annotations/"
output_dir = "labels/"
image_dir = "C:/Users/Salih/Desktop/Teknofest UYZ 2021 Etiketli Veriler/images"

# create the labels folder (output directory)
if os.path.isdir(output_dir):
    shutil.rmtree(output_dir)
os.mkdir(output_dir)

# identify all the xml files in the annotations folder (input directory)
files = glob.glob(os.path.join(input_dir, '*.xml'))
# loop through each
for fil in files:
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    # check if the label contains the corresponding image file
    if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):
        print(f"{filename} image does not exist!")
        continue

    result = []

    # parse the content of the xml file
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)
    height = int(root.find("size").find("height").text)

    for obj in root.findall('object'):
        label = obj.find("name").text
        if label == "UAP":
            label = "uap"
            index = 2
        elif label == "UAİ":
            label = "uai"
            index = 4
        elif label == "İnsan":
            label = "pedestrian"
            index = 0
        elif label == "Taşıt":
            label = "vehicle"
            index = 1
            # check for new classes and append to list

        if label in ["uap", "uai"]:
            object_attributes = {}
            descendable = None
            for attr in obj.find("attributes").findall("attribute"):
                attribute = [a.text for a in attr]
                object_attributes[attribute[0]] = attribute[1]
                # for a in attr:
                #     print(a.text)
                # print("break")
            if object_attributes["İnilebilir"] == "True":
                index += 1
                descendable = True
            else:
                descendable = False

            if not descendable:
                label += "_not"
                # value = attr.find("name").text
                # if value is not None:
                #     print(value)
        # elif label == "uai":
        #     for attr in obj.find("attributes").find("attribute"):
        #         value = obj.find("attributes").items()
                # if value is not None:
                #     print(value)
        # try:
        #     for attr in obj.find("attributes").find("attribute"):
        #         value = attr.find("value")
        #         if value is not None:
        #             print(value)
        # except:
        #     print(fil)
        #     print(sys.exc_info())

        # if label not in classes:
        #     classes.append(label)

        # index = classes.index(label)
        pil_bbox = [float(x.text) for x in obj.find("bndbox")]
        yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
        # convert data to string
        bbox_string = " ".join([str(x) for x in yolo_bbox])

        if index in [0, 1]:
            result.append(f"{index} {bbox_string}")

    if result:
        # generate a YOLO format text file for each xml file
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result))

# generate the classes file as reference
with open('classes.txt', 'w', encoding='utf8') as f:
    for c in classes:
        f.write(c + "\n")