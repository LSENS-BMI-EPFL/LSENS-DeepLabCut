import os
import sys
import deeplabcut as dlc

def run_dlc_anly():

    args = sys.argv(1)

    session_to_anly = ["PB175_20240311_170817"]
    date_to_anly = None

    config_path = os.path.join("/scratch", "izar", "bechvila", "context_dlc_sideview-PB-2024-02-21/config.yaml")
    video_folder = os.path.join("/scratch", "izar", "bechvila", "videos_to_anly")
    dest_folder = os.path.join("/scratch", "izar", "bechvila", "dlc_results")

    dlc.analyze_video(config_path,
                      video_folder + session_to_anly[0] + '_sideview.avi',
                      videotype="avi",
                      save_as_csv=False,
                      dest_folder=dest_folder)
