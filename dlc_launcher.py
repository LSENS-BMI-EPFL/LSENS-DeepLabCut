import os
import sys
import json
import shutil
import subprocess


def launch_dlc():
    user = sys.argv[1]
    json_name = sys.argv[2]

    json_path = os.path.join("/home", user, "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)

    video_folder = f"/scratch/{user}/videos_to_anly"
    result_folder = f"/scratch/{user}/dlc_results"

    for vid in json_config["videos_to_anly"]:
        vid_name = vid.split("/")[-1][:-4].replace(" ", "_")
        extension = vid.split("/")[-1][-4:]

        dest_folder = os.path.join(result_folder, vid_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder, exist_ok=True)

        command = f" {json_config['config_path']} {os.path.join(video_folder, vid_name + extension)} {dest_folder}"
        print(f"Executing command: {command}")
        subprocess.run(["echo", f"INFO: Launching dlc for video {vid_name}"])

        os.system(f"sbatch /home/{user}/LSENS-DeepLabCut/launch_dlc.sbatch" + command)


if __name__ == "__main__":
    launch_dlc()