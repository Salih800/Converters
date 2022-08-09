import shutil
import time

import cv2
import os


video_path = "/path/to/video/file"
cap = cv2.VideoCapture(video_path)

width, height, fps, frame_count = int(cap.get(3)), int(cap.get(4)), cap.get(5), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

zfill_count = len(str(frame_count))
jpg_save_quality = 50

print(f"width: {width}, height: {height}, fps: {fps}, frame_count: {frame_count}")

frames_folder = os.path.basename(video_path) + "_frames/"
if os.path.isdir(frames_folder):
    shutil.rmtree(frames_folder)
os.makedirs(frames_folder)

frame_number = 0
start_time = time.time()
while True:
    ret, img = cap.read()
    if not ret:
        print(f"Video ended. Total {frame_number} frame extracted in {round(time.time() - start_time, 2)} seconds")
        break
    frame_name = "frame_" + str(frame_number).zfill(zfill_count) + ".jpg"
    cv2.imwrite(frames_folder + frame_name, img, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_save_quality])
    frame_number += 1
    print(f"{frame_number}/{frame_count} Frame extracted.")
    
