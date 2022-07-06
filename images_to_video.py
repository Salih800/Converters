import os
import cv2
import glob
from natsort import natsorted
import imutils

folder_path = "C:/Users/Salih/Desktop/visdrone_dataset/images/"
folder_name = "val"

pics_list = natsorted(glob.glob(os.path.join(folder_path + folder_name + "/*")))

set_fps = 15
fourcc = "mp4v"

video_file_path = folder_name + ".mp4"
record_width, record_height = (1920, 1080)

out = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*fourcc),
                      set_fps, (record_width, record_height))

print(pics_list)
for pic in pics_list:
    print(pic)
    img = cv2.imread(pic)
    img = imutils.resize(img, width=record_width, height=record_height)
    out.write(img)

out.release()
