import os
import cv2
import glob
from natsort import natsorted
import imutils

folder_path = "/path/to/images/folder/"
folder_name = "folder_name"

file_formats = ["jpg", "jpeg", "png"]

pics_list = []
for file_format in file_formats:
    format_list = glob.glob(os.path.join(folder_path + folder_name + "/*." + file_format))
    pics_list.append(format_list)

pics_list = natsorted(pics_list)

set_fps = 15
fourcc = "mp4v"

video_file_path = folder_name + "_merged.mp4"
record_width, record_height = (1280, 720)

out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*fourcc),
                      set_fps, (record_width, record_height))

print(f"Total {len(pics_list)} picture found")
for i, pic in enumerate(pics_list):
    print(f"{i+1}/{len(pics_list)}", pic)
    img = cv2.imread(pic)
    img = imutils.resize(img, width=record_width, height=record_height)
    out.write(img)

out.release()
