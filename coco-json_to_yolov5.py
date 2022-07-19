import json
import cv2
import os
import shutil


def get_img_shape(path):
    img = cv2.imread(path)
    try:
        return img.shape
    except AttributeError:
        print("error! ", path)
        return None, None, None


def convert_labels(path, x1, y1, x2, y2):
    """"
    Definition: Parses label files to extract label and bounding box
    coordinates. Converts (x1, y1, x1, y2) KITTI format to
    (x, y, width, height) normalized YOLO format.
    """
    def sorting(l1, l2):
        if l1 > l2:
            lmax, lmin = l1, l2
            return lmax, lmin
        else:
            lmax, lmin = l2, l1
            return lmax, lmin
    size = get_img_shape(path)
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1./size[1]
    dh = 1./size[0]
    x = (xmin + xmax)/2.0
    y = (ymin + ymax)/2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x, y, w, h

annotations_folder = "annotations"
label_folder = "mylabels/train"
image_folder = "images/train2017"
training_data = json.load(open(annotations_folder + "/instances_train2017.json"))

check_set = set()

if os.path.isdir(label_folder):
    shutil.rmtree(label_folder)
os.makedirs(label_folder)

for i in range(len(training_data['annotations'])):
    image_id = str(training_data['annotations'][i]['image_id']).zfill(12)
    category_id = str(training_data['annotations'][i]['category_id'])
    if category_id in ["1", "3", "4", "6", "7", "8"]:
        if category_id != "1":
            category_id = "1"
        else:
            category_id = "0"
        bbox = training_data['annotations'][i]['bbox']
        image_path = image_folder + "/" + image_id + ".jpg"
        kitti_bbox = [bbox[0], bbox[1], bbox[2] + bbox[0], bbox[3] + bbox[1]]
        yolo_bbox = convert_labels(image_path, kitti_bbox[0], kitti_bbox[1], kitti_bbox[2], kitti_bbox[3])
        filename = image_id + ".txt"
        content = category_id + " " + str(yolo_bbox[0]) + " " + str(yolo_bbox[1]) + " " + str(yolo_bbox[2]) + " " + str(yolo_bbox[3])
        #print(filename, content)
        if image_id in check_set:
            # Append to file files
            file = open(label_folder + "/" + filename, "a")
            file.write("\n")
            file.write(content)
            file.close()
        elif image_id not in check_set:
            check_set.add(image_id)
            # Write files
            file = open(label_folder + "/" + filename, "w")
            file.write(content)
            file.close()

