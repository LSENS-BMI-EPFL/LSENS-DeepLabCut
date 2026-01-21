import os
import sys
import json
import glob
import shutil
import subprocess
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def transfer_results():
    user = sys.argv[1]
    json_name = sys.argv[2]

    json_path = os.path.join("/home", user, "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)
    view = json_name.split("_")[0]
    result_folder = f"/scratch/{user}/dlc_results"
    dest_folder = f"/home/{user}/servers"
    vid_folder = f"/scratch/{user}/videos_to_anly"

    for vid, result in zip(json_config["videos_to_anly"], json_config["server_dest_folder"]):
        vid_name = os.path.splitext(vid)[0].split("/")[-1]
        print(f"Processing {vid_name}... ")

        result_path = os.path.join(result_folder, vid_name)
        save_path = os.path.join(dest_folder, result, 'sideview' if 'side' in vid_name else 'topview')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            os.makedirs(os.path.join(save_path, 'plot-poses'))

        files = [file for file in glob.glob(os.path.join(result_path, '*.csv')) if os.path.isfile(file)]            
        files = [file for file in files if 'split' in file]

        raw_data = [file for file in files if "filtered" not in file]
        raw_data.sort(key=lambda fname: int(os.path.splitext(fname)[0].split('split')[1].split("DLC")[0]))
        data_to_save = []
        for file in raw_data:
            data = pd.read_csv(file, header=[1,2])
            data['split'] = file.split('split')[1].split('DLC')[0]
            data_to_save.append(data)
        data_to_save = pd.concat(data_to_save)
        data_to_save.to_csv(os.path.join(result_path, f"{vid_name}.csv"))        
        data_to_save.to_csv(os.path.join(save_path, f"{vid_name}.csv"))

        filtered_data = [file for file in files if "filtered" in file]
        filtered_data.sort(key=lambda fname: int(os.path.splitext(fname)[0].split('split')[1].split("DLC")[0]))
        data_to_save = []
        for file in raw_data:
            data = pd.read_csv(file, header=[1,2])
            data['split'] = file.split('split')[1].split('DLC')[0]
            data_to_save.append(data)
        data_to_save = pd.concat(data_to_save)
        data_to_save.to_csv(os.path.join(result_path, f"{vid_name}_filtered.csv"))        
        data_to_save.to_csv(os.path.join(save_path, f"{vid_name}_filtered.csv"))

        folder = [dir for dir in glob.glob(os.path.join(result_path, '*')) if os.path.isdir(dir)]
        for f in folder:
            if "plot-poses" in f:     
                subprocess.call(f"cp -r {f} {os.path.join(save_path, 'plot-poses')}", shell=True)   
                # shutil.copytree(f, os.path.join(save_path, 'plot-poses'), dirs_exist_ok=True, copy_function=shutil.copy)
            elif "split_videos" in f:
                shutil.rmtree(f)
            else:
                print(f"{f} not found")
        
    return


if __name__ == "__main__":
    transfer_results()