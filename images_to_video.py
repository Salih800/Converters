import os
import cv2
import glob
from natsort import natsorted
import imutils

folder_path = "E:/github-repos/Sorax-Live/"
folder_name = "saved_images"

pics_list = natsorted(glob.glob(os.path.join(folder_path + folder_name + "/*")))

set_fps = 15
fourcc = "mp4v"

video_file_path = folder_name + ".mp4"
record_width, record_height = (1920, 1080)

out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*fourcc),
                      set_fps, (record_width, record_height))

# print(pics_list)
for i, pic in enumerate(pics_list):
    print(f"{i+1}/{len(pics_list)}", pic)
    img = cv2.imread(pic)
    img = imutils.resize(img, width=record_width, height=record_height)
    out.write(img)

out.release()
