import os
import sys
import json
import timeit
import shutil
import deeplabcut as dlc

def test():

    user = sys.argv[1]
    print(user)
    json_path = sys.argv[2]
    print(user, json_path)
    with open(json_path, 'r') as f:
        json_config = json.load(f)

    # config_path = os.path.join("/scratch", "izar", "bechvila", "context_dlc_sideview-PB-2024-02-21/config.yaml")
    dest_folder = os.path.join("/scratch", "izar", user, "dlc_results")
    server_folder = os.path.join("/home", user, "servers")

    if not os.path.exists(json_config['config_path']):
        ValueError("DLC config.yaml not found")
        return 1

    for video, server_dest in zip(json_config['videos_to_anly'], json_config['server_dest_folder']):
        print(f"Session to anly is in folder: {os.path.exists(video)}{', skipping' if not os.path.exists(video) else ''}")
        print(os.path.join(server_folder, video))
    # user = sys.argv[1]
    # # json_path = sys.argv[2]
    # with open(json_path, 'r') as f:
    #     json_config = json.load(f)
    # print(user, json_config['videos_to_anly'][0])

if __name__ == "__main__":
    test()