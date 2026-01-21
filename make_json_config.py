import os
import csv
import json
import yaml
from datetime import datetime

def make_json_for_dlc(experimenter, camera_view, sessions_to_anly: list, save_name):
    """Script to generate a json config file that would serve to run batch videos for DLC
    Arguments:
        experimenter : as in analysis folder
        camera_view : 'sideview' or 'topview'
        sessions_to_anly : list of session names
    """
    if experimenter not in ["Anthony_Renard", "Axel_Bisi", "Lana_Smith", "Mauro_Pulin", "Meriam_Malekzadeh", "Pol_Bech", "Robin_Dard"]:
        ValueError("Experimenter not in list")

    if camera_view not in ['sideview', 'topview']:
        ValueError("Camera view not supported, must be either 'sideview' or 'topview'")

    path_list = []
    analysis_dir_list = []
    for session in sessions_to_anly:
        mouse_id = session.split('_')[0]
        path = os.path.join(r"\\sv-nas1.rcp.epfl.ch", "Petersen-Lab", "data", mouse_id, "Recording", "Video", session, f"{session}_{camera_view}.avi")
        # if not os.path.isfile(path):
        #     continue

        path_list += [os.path.join("data", mouse_id, "Recording", "Video", session, session+ f"_{camera_view}.avi").replace("\\", "/")]

        analysis_dir_list += [os.path.join("analysis", experimenter, "data", mouse_id, session).replace("\\", "/")]

    to_json = {
        "config_path": fr"/home/bechvila/LSENS-DeepLabCut/context_{'side' if 'side' in camera_view else 'top'}_dlc-PB-2025-01-09/config.yaml",
        "videos_to_anly": path_list,
        "server_dest_folder": analysis_dir_list
    }
    with open(fr"./json_files/{save_name}.json", "w", encoding='utf-8') as f:
        json.dump(to_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    filter_by_date = False
    sessions_from_file = True
    # mouse_id = ["RD039", "RD040", "RD041", "RD042", "RD043", "RD044", "RD045"]
    date_to_anly = ["20240609", "20240610", "20240611", "20240612"]
    # mouse_id = ['PB176', 'PB177', 'PB178', 'PB179', 'PB181', 'PB182', "PB184"]
    mouse_id = None

    if filter_by_date == True and date_to_anly is None:
        ValueError("Introduce a valid date or set filter to False")

    # with open(os.path.join("/home/bechvila/servers", "z_LSENS", "Share", "Pol_Bech", "Session_list",
    #                        "side_train_list.csv"), newline="") as file:
    #     reader = csv.reader(file)
    #     video_list = list(reader)[0]

    config_file = r"/home/bechvila/servers/z_LSENS/Share/Pol_Bech/Session_list/context_sessions_wf_opto_controls.yaml"
    with open(config_file, 'r', encoding='utf8') as stream:
        config_dict = yaml.safe_load(stream)
    sessions_to_anly = config_dict['Session id']

    experimenter = "Pol_Bech"

    for camera_view in ['sideview', 'topview']:
        today = datetime.today().strftime('%Y%m%d_%H%M%S')
        save_name = f"{camera_view}_dlc_config_{date_to_anly if filter_by_date else today}"

        # if sessions_from_file:
        #     sessions_to_anly = [vid.split("\\")[-2]for vid in video_list]

        # else:
        #     sessions_to_anly = []

        #     for mouse in mouse_id:
        #         mouse_folder = os.listdir(os.path.join(r"//sv-nas1.rcp.epfl.ch", "Petersen-lab", "data", mouse, "Recording", "Video"))

        #         if filter_by_date:
        #             for date in date_to_anly:
        #                 sessions_to_anly += [folder for folder in mouse_folder if date in folder]
        #         else:
        #             sessions_to_anly += mouse_folder

        make_json_for_dlc(experimenter=experimenter,
                          camera_view=camera_view,
                          sessions_to_anly=sessions_to_anly,
                          save_name=save_name)