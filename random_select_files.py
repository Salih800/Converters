import glob
import os
import shutil

pics = "pics"
pics2 = "pics2"

labels1 = "labels1"
labels2 = "labels2"

if os.path.isdir(pics):
    shutil.rmtree(pics)
os.mkdir(pics)

if os.path.isdir(pics2):
    shutil.rmtree(pics2)
os.mkdir(pics2)

if os.path.isdir(labels1):
    shutil.rmtree(labels1)
os.mkdir(labels1)

if os.path.isdir(labels2):
    shutil.rmtree(labels2)
os.mkdir(labels2)

file_path = "C:/Users/Salih/Desktop/Teknofest UYZ 2021 Etiketli Veriler/images/*"

file_list = glob.glob(file_path)
i = 0
for file in file_list:
    if i == 0:
        i += 1
        shutil.copy(file, os.path.join(pics, os.path.basename(file)))
    else:
        i = 0
        shutil.copy(file, os.path.join(pics2, os.path.basename(file)))
