import deeplabcut as dlc
import os
import sys


def train_dlc_network():
    #config_path = sys.argv[1]
    #os.system("echo " + config_path)
    config_path = os.path.join("/home", "bechvila", "LSENS-DeepLabCut", "context_side_dlc-PB-2025-01-09/config.yaml").replace("\\", "/")

    if not os.path.exists(config_path):
        ValueError("Config path not found")
        exit(1)

    dlc.create_training_dataset(config_path)
    dlc.train_network(config_path,
                      shuffle=1,
                      trainingsetindex=0,
                      gputouse=1,
                      max_snapshots_to_keep=5,
                      autotune=False,
                      displayiters=1000,
                      allow_growth=True)
    dlc.evaluate_network(config_path, plotting=True)

if __name__ == "__main__":
    train_dlc_network()