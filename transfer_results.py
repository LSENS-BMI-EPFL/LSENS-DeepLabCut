import os
import sys
import json
import shutil


def transfer_results():
    user = sys.argv[1]
    json_name = sys.argv[2]

    json_path = os.path.join("/home", user, "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)

    view = json_name.split("_")[0]
    result_folder = f"/scratch/izar/{user}/dlc_results"
    dest_folder = f"/home/{user}/servers"
    vid_folder = f"/scratch/izar/{user}/videos_to_anly"

    for vid, result in zip(json_config["videos_to_anly"], json_config["server_dest_folder"]):
        vid_name = vid.split("/")[-1]

        if os.path.exists(os.path.join(vid_folder, vid_name)):
           os.remove(os.path.join(vid_folder, vid_name))

        for item in os.listdir(os.path.join(result_folder, vid_name[:-4])):
            print(f"Copying data from: {os.path.join(result_folder, vid_name[:-4], item)} to: {os.path.join(dest_folder, result, view)}")
            if not os.path.exists(os.path.join(dest_folder, result, view)):
                os.makedirs(os.path.join(dest_folder, result, view))

            shutil.copyfile(os.path.join(result_folder, vid_name[:-4], item), os.path.join(dest_folder, result, view, item))
        
    return


if __name__ == "__main__":
    transfer_results()