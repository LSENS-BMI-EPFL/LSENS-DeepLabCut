import os
import sys
import json
import csv
import subprocess


def transfer_data():
    user = sys.argv[1]
    json_name = sys.argv[2]

    json_path = os.path.join("/home", user, "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)

    server_path = f"/home/{user}/servers"
    dest_folder = f"/scratch/{user}/videos_to_anly/"
    log_path = f"/home/{user}/logs/{os.path.splitext(json_name)[0]}_transfer_log.csv"

    with open('source.txt', 'w', newline='') as f:
        writer = csv.writer(f)
        for item in json_config['videos_to_anly']:
            writer.writerow([item])

    cmd = f"rsync -av --progress --no-relative --files-from='source.txt' {server_path + '/'} {user}@kuma.hpc.epfl.ch:{dest_folder} | tee {log_path}"

    os.system(cmd)

if __name__ == "__main__":
    transfer_data()