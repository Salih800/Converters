import glob
import os
import shutil

labels_path = "/path/to/labels/"

labels_list = glob.glob(labels_path + "*.txt")

input_classes = ["uap", "pedestrian", "vehicle", "uap_not", "uai_not", "uai"]
output_classes = ["pedestrian", "vehicle"]

mapped_classes = {}

for i, icls in enumerate(input_classes):
    for j, ocls in enumerate(output_classes):
        if icls == ocls:
            mapped_classes[str(i)] = str(j)            
        
print(mapped_classes)

new_labels_path = "./_changed_labels/"
if os.path.isdir(new_labels_path):
    shutil.rmtree(new_labels_path)
os.makedirs(new_labels_path)

for label_file in labels_list:
    label_file_name = os.path.basename(label_file)
    with open(label_file) as file:
        yolo_labels = []
        for line in file.readlines():
            class_id, x, y, w, h = line.split()
            try:
                yolo_labels.append({"class_id": mapped_classes[class_id], "x": x, "y": y, "w": w, "h": h})
            except:
                print(f"Invalid Class: {label_file}\n\t{class_id}")
                continue
    with open(new_labels_path + label_file_name, "a+") as new_label_file:
        for label in yolo_labels:
            temp = f"{label['class_id']} {label['x']} {label['y']} {label['w']} {label['h']}"

            new_label_file.write(f"{temp}\n")

    print(f"{label_file}: Total Labels: {len(yolo_labels)}")