import glob
import os
import shutil
import time

import cv2
from PIL import Image, ImageDraw, ImageFont


def draw_bounding_boxes(image_path, json_result_list):
    frame_id = int(image_path[:-4].split("_")[-1])
    detected_images_folder = "./_detected_images/"
    if not os.path.isdir(detected_images_folder):
        os.mkdir(detected_images_folder)

    font = ImageFont.truetype(r'arial.ttf', 15)
    img = Image.open(image_path).convert("RGBA")
    img_shape = img.size
    draw = ImageDraw.Draw(img)
    for json_result in json_result_list[frame_id]:
        label = f"{json_result['track_id']}-{json_result['lost']}{json_result['occluded']}{json_result['generated']}"
        w, h = font.getsize(label)
        draw.rectangle((json_result["xmin"], json_result["ymin"],
                        min(img_shape[0] - 1, json_result["xmax"]),
                        min(img_shape[1] - 1, json_result["ymax"])),
                       outline=(255, 0, 0), width=2)

        draw.rectangle((json_result["xmin"], json_result["ymin"],
                        json_result["xmin"] + w, json_result["ymin"] - h),
                       outline=(255, 0, 0), width=2, fill=(255, 0, 0))

        draw.text((json_result["xmin"], json_result["ymin"] - h), label, font=font)

    detected_image_path = detected_images_folder[:-1] + image_path
    if not os.path.isdir(os.path.dirname(detected_image_path)):
        os.makedirs(os.path.dirname(detected_image_path))
    img.convert("RGB").save(detected_image_path)
    cv2.imshow("FRAME", cv2.imread(detected_image_path))
    cv2.waitKey(1)


def convert_labels(x1, y1, x2, y2, cls, frame_size):
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

    size = frame_size
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (xmin + xmax) / 2.0
    y = (ymin + ymax) / 2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return cls, x, y, w, h


def write_label(l, label_file_path):
    with open(label_file_path, "a") as label_file:
        label_file.write(f"{l[0]} {l[1]} {l[2]} {l[3]} {l[4]}\n")


frame_namer = "_frame_"
path = "C:/Users/Salih/Desktop/archive/"
save_path = "stanford_dataset/"

images_save_path = save_path + "images/"
labels_save_path = save_path + "labels/"

if os.path.isdir(images_save_path):
    shutil.rmtree(images_save_path)
if os.path.isdir(labels_save_path):
    shutil.rmtree(labels_save_path)

os.makedirs(images_save_path)
os.makedirs(labels_save_path)


annotation_folders = glob.glob(path + "annotations/*/")
video_folders = glob.glob(path + "video/*/")

total_frames = 0
for video_folder, annotation_folder in zip(video_folders, annotation_folders):
    # print(video_folder, annotation_folder)
    for video_path, annotation_path in zip(glob.glob(video_folder+"./*/"), glob.glob(annotation_folder+"./*/")):

        splitted_path = video_path.split("/")[-1].split("\\")
        video_name = video_path + "video.mp4"

        cap = cv2.VideoCapture(video_name)
        fps = cap.get(5)
        width, height = cap.get(3), cap.get(4)

        print(video_name)
        print(width, height, fps)

        frame_counter = 0
        while True:
            frame_count = int(cap.get(1))
            ret, img = cap.read()
            if not ret:
                print(f"Total pictures: {frame_counter}")
                break
            if frame_count >= (fps * 2 * frame_counter):
                frame_counter += 1
                frame_name = f"{images_save_path}{splitted_path[1]}-{splitted_path[3]}" \
                             f"{frame_namer}{str(frame_count).zfill(6)}.jpg"
                cv2.imwrite(frame_name, img)
                # cv2.waitKey(1)
        total_frames += frame_counter

        splitted_path = annotation_path.split("/")[-1].split("\\")
        annotation_name = annotation_path + "annotations.txt"
        with open(annotation_name) as file:
            data = file.readlines()

        frame_results = {}

        for line in data:
            track_id, xmin, ymin, xmax, ymax, frame, lost, occluded, generated, label = line.split()

            json_label = {"track_id": int(track_id), "xmin": int(xmin), "ymin": int(ymin),
                          "xmax": int(xmax), "ymax": int(ymax), "frame": int(frame), "lost": int(lost) == 1,
                          "occluded": int(occluded) == 1, "generated": int(generated) == 1, "label": label}
            try:
                frame_results[json_label["frame"]].append(json_label)
            except:
                frame_results[json_label["frame"]] = [json_label]

            if not json_label["lost"]:

                if json_label["label"] == '"Pedestrian"':
                    json_label["cls"] = 0
                else:
                    json_label["cls"] = 0

                yolo_label = convert_labels(x1=json_label["xmin"],
                                            y1=json_label["ymin"],
                                            x2=json_label["xmax"],
                                            y2=json_label["ymax"],
                                            cls=json_label["cls"],
                                            frame_size=(width, height))

                label_name = f"{labels_save_path}{splitted_path[1]}-{splitted_path[3]}" \
                             f"{frame_namer}{str(json_label['frame']).zfill(6)}.txt"
                write_label(yolo_label, label_name)

print(f"Total Saved Photos: {total_frames}")
        # print(video_name.split("/")[-1].split("\\"), annotation_name)



# saved_labels_path = "yolo_labels/"
# if os.path.isdir(saved_labels_path):
#     shutil.rmtree(saved_labels_path)
# os.makedirs(saved_labels_path)

# folder_name = "hyang-video6/"
# video_file = folder_name + "video.mp4"
# annotation_file = folder_name + "annotations.txt"
#
# frame_namer = "frame_"
#
# images_path = video_file.split("/")[0] + "/images/"
# labels_path = video_file.split("/")[0] + "/labels/"
#
# if os.path.isdir(images_path):
#     shutil.rmtree(images_path)
# if os.path.isdir(labels_path):
#     shutil.rmtree(labels_path)
# os.makedirs(images_path)
# os.makedirs(labels_path)
#
# labels_of_file = []
# with open(annotation_file) as file:
#     data = file.readlines()
#
# frame_results = {}
#
# cap = cv2.VideoCapture(video_file)
#
# while True:
#     frame_count = int(cap.get(1))
#     ret, img = cap.read()
#     if not ret:
#         print(ret)
#         break
#     cv2.imwrite(f"{images_path}{frame_namer}{str(frame_count).zfill(6)}.jpg", img)
#     cv2.waitKey(1)
#
# for line in data:
#     track_id, xmin, ymin, xmax, ymax, frame, lost, occluded, generated, label = line.split()
#
#     json_label = {"track_id": int(track_id), "xmin": int(xmin), "ymin": int(ymin),
#                   "xmax": int(xmax), "ymax": int(ymax), "frame": int(frame), "lost": int(lost) == 1,
#                   "occluded": int(occluded) == 1, "generated": int(generated) == 1, "label": label}
#     try:
#         frame_results[json_label["frame"]].append(json_label)
#     except:
#         frame_results[json_label["frame"]] = [json_label]
#
#     # print(json_label)
#     labels_of_file.append(json_label)
#     if not json_label["lost"]:
#
#         if json_label["label"] == '"Pedestrian"':
#             json_label["cls"] = 0
#         else:
#             json_label["cls"] = 1
#         # print(frame_results)
#         # time.sleep(1)
#
#         yolo_label = convert_labels(x1=json_label["xmin"],
#                                     y1=json_label["ymin"],
#                                     x2=json_label["xmax"],
#                                     y2=json_label["ymax"],
#                                     cls=json_label["cls"])
#
#         write_label(yolo_label, json_label["frame"])

# print(frame_results)
# image_list = glob.glob(images_path + "*.jpg")
# for image in image_list:
#     print(image)
#     draw_bounding_boxes(image_path=image, json_result_list=frame_results)
    # print(*yolo_label)
# print(len(labels_of_file))
