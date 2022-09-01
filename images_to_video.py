import os
import cv2
import glob
from natsort import natsorted
import argparse


def main(args):
    folder_path = args.folder_path
    video_save_name = args.save_name if args.save_name else os.path.basename(folder_path) + ".mp4"

    if "*" not in folder_path:
        file_formats = ["jpg", "jpeg", "png"]

        pics_list = []
        for file_format in file_formats:
            format_list = glob.glob(os.path.join(folder_path + "/*." + file_format))
            if len(format_list) > 0:
                pics_list += format_list
    else:
        pics_list = glob.glob(folder_path)

    pics_list = natsorted(pics_list)

    set_fps = args.fps
    fourcc = args.codec

    record_width, record_height = (args.width, args.height)

    out = cv2.VideoWriter(video_save_name, cv2.VideoWriter_fourcc(*fourcc),
                          set_fps, (record_width, record_height))

    print(f"Total {len(pics_list)} picture found")
    for i, pic in enumerate(pics_list):
        print(f"{i + 1}/{len(pics_list)}", pic)
        img = cv2.imread(pic)
        img = cv2.resize(img, (record_width, record_height))
        out.write(img)

    out.release()


# construct the argument parser and parse the arguments
def arg_parse():
    parser = argparse.ArgumentParser(description="Merge images to video")
    parser.add_argument("--folder_path", type=str, default="", help="Path to folder")
    parser.add_argument("--fps", type=int, default=10, help="FPS")
    parser.add_argument("--codec", type=str, default="mp4v", help="Codec")
    parser.add_argument("--width", type=int, default=1280, help="Width")
    parser.add_argument("--height", type=int, default=720, help="Height")
    parser.add_argument("--save_name", type=str, default="", help="Save name")
    return parser.parse_args()


if __name__ == "__main__":
    main(arg_parse())
