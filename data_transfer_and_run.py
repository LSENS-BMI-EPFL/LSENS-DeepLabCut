import os
import sys
import json
import shutil
import subprocess


def transfer_data():
    user = sys.argv[1]
    json_name = sys.argv[2]

    json_path = os.path.join("/home", user, "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)

    server_path = f"/home/{user}/servers"
    video_folder = f"/scratch/izar/{user}/videos_to_anly"
    result_folder = f"/scratch/izar/{user}/dlc_results"

    for vid, result in zip(json_config["videos_to_anly"], json_config["server_dest_folder"]):
        vid_name = vid.split("/")[-1][:-4]
        origin = os.path.join(server_path, vid)
        dest_folder = os.path.join(result_folder, vid_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder, exist_ok=True)

        shutil.copy(origin, video_folder)
        subprocess.run(["sbatch", f"/home/{user}/LSENS-DeepLabCut/analyze_video.sbatch", f"{json_config['config_path']}", os.path.join(video_folder, vid_name, ".avi"), f"{dest_folder}"])

if __name__ == "__main__":
    transfer_data()
