import glob
import os
from natsort import natsorted

files_path = "C:/Users/Salih/Desktop/gonderilecek_veriler/B160519_V1_K1/*"

files_list = glob.glob(files_path)

files_list = natsorted(files_list)

for file in files_list:
    print(file)

# for file in os.listdir(sorted(files_path)):
#     print(file)