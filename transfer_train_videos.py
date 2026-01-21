import os
import csv
import shutil
import subprocess

def transfer_vids(video_list):
    dest_root = "/scratch/bechvila/videos_to_anly"

    for vid in video_list:
        vid_name = vid.split("/")[-1]
        dest = os.path.join(dest_root, vid_name)
        if not os.path.exists(vid):
            print(f"Video not found: {vid}")
        elif not os.path.exists(dest_root):
            print(f"Dest not found: {dest_root}")


        if not os.path.exists(os.path.join(dest_root, vid_name)):
            print(f"Copying data from: {vid} to: {dest}")
            shutil.copy(vid, dest)


    return
if __name__ == "__main__":

    with open(os.path.join("/home/bechvila/servers", "z_LSENS", "Share", "Pol_Bech", "Session_list",
                           "top_train_list.csv"), newline="") as file:
        reader = csv.reader(file)
        video_list = list(reader)[0]

    #with open(os.path.join("/home/bechvila/servers", "z_LSENS", "Share", "Pol_Bech", "Session_list",
     #                      "top_train_list.csv"), newline="") as file:
      #  reader = csv.reader(file)
       # video_list.extend(list(reader)[0])

    video_list = [file.replace("M:", "\\home\\bechvila\\servers") for file in video_list]
    video_list = [file.replace("\\", "/") for file in video_list]

    transfer_vids(video_list)