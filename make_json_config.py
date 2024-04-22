import os
import json
from datetime import datetime
def make_json_for_dlc(experimenter, camera_view, sessions_to_anly: list):
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
        path = os.path.join(r"\\sv-nas1.rcp.epfl.ch", "Petersen-Lab", "data", mouse_id, "Recording", "Video", session, session+ f"_{camera_view}.avi")
        if not os.path.isfile(path):
            continue

        path_list += [os.path.join("data", mouse_id, "Recording", "Video", session, session+ f"_{camera_view}.avi").replace("\\", "/")]

        analysis_dir_list += [os.path.join("analysis", experimenter, "data", mouse_id, session).replace("\\", "/")]

    to_json = {
        "config_path": fr"/scratch/izar/bechvila/context_dlc_{camera_view}-PB-2024-02-21/config.yaml",
        "videos_to_anly": path_list,
        "server_dest_folder": analysis_dir_list
    }
    today = datetime.today().strftime('%Y%m%d_%H%M%S')
    with open(fr"./json_files/{camera_view}_dlc_config_{today}.json", "w", encoding='utf-8') as f:
        json.dump(to_json, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":

    filter_by_date = False
    # mouse_id = ["RD039", "RD040", "RD041", "RD042", "RD043", "RD044", "RD045"]
    date_to_anly = ["20240210", "20240212"]
    mouse_id = ['PB173', 'PB174', 'PB175']
    # date_to_anly = ["20240220", "20240222"]
    if filter_by_date == True and date_to_anly is None:
        ValueError("Introduce a valid date or set filter to False")

    camera_view = 'sideview'
    experimenter = "Pol_Bech"

    sessions_to_anly = []

    for mouse in mouse_id:
        mouse_folder = os.listdir(os.path.join(r"//sv-nas1.rcp.epfl.ch", "Petersen-lab", "data", mouse, "Recording", "Video"))

        if filter_by_date:
            for date in date_to_anly:
                sessions_to_anly += [folder for folder in mouse_folder if date in folder]
        else:
            sessions_to_anly += mouse_folder


    make_json_for_dlc(experimenter=experimenter,
                      camera_view=camera_view,
                      sessions_to_anly=sessions_to_anly)