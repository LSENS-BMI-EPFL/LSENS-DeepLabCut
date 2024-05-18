import os
import cv2
import json
import tifffile
import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from PIL import Image
from tqdm import tqdm
from random import sample
from scipy.signal import find_peaks

def check_dlc(vid, file, view, make_video=False, parts_to_make_clips=['tongue_y']):

    save_path = file.replace(file.split("/")[-1], "dlc_check").replace("\\", "/")
    # save_path = r"M:\analysis\Pol_Bech\Pop_results\Context_behaviour".replace("\\", "/")
    if not os.path.exists(os.path.join(save_path, 'temp')):
        os.makedirs(os.path.join(save_path, 'temp'), exist_ok=True)

    print(f"Opening data for video: {file.split('/')[-1]}")
    video = cv2.VideoCapture(vid)
    data = pd.read_csv(file, header=[1, 2])

    bodyparts = np.unique([item[0] for item in data.keys() if item[0] != 'bodyparts'])

    print("Generating summary plots")
    fig, ax = plt.subplots(3, 4, figsize=(12, 12), sharex=True)
    fig.suptitle("Likelihood over time")

    fig1, ax1 = plt.subplots(3, 4, figsize=(12, 12), sharex=True, sharey=True)
    fig1.suptitle("Likelihood distributions")

    fig2, ax2 = plt.subplots(3, 4, figsize=(12, 12), sharex=True, sharey=True)
    fig2.suptitle("X Y pixel position over time")

    for i, bodypart in enumerate(bodyparts):
        if bodypart == 'bodyparts':
            continue
        # print(f"Analyzing the following bodypart: {bodypart}")

        ax.flat[i].plot(data[bodypart]['likelihood'])
        ax.flat[i].scatter(data.shape[0] + 1000, data[bodypart]['likelihood'].mean(), s=50, c='r')
        ax.flat[i].errorbar(data.shape[0]+ 1000, data[bodypart]['likelihood'].mean(), yerr=data[bodypart]['likelihood'].std())
        ax.flat[i].set_ylim(-0.05,1.05)
        ax.flat[i].set_xlabel("Frames")
        ax.flat[i].set_title(bodypart)

        ax1.flat[i].hist(data[bodypart]['likelihood'], bins=25)
        ax1.flat[i].set_xlim(-0.05, 1.05)
        ax1.flat[i].set_ylabel("Counts")
        ax1.flat[i].set_title(bodypart)

        ax2.flat[i].plot(np.where(data[bodypart]['likelihood'] > 0.6, data[bodypart]['y'], np.nan), label='y')
        ax2.flat[i].plot(np.where(data[bodypart]['likelihood'] > 0.6, data[bodypart]['x'], np.nan), label='x')
        ax2.flat[i].set_ylabel("Pixels")
        ax2.flat[i].set_xlabel("Frames")
        ax2.flat[i].set_title(bodypart)

    fig.tight_layout()
    fig1.tight_layout()
    fig2.tight_layout()
    fig2.legend()

    for ext in [".png", ".svg"]:
        fig.savefig(os.path.join(save_path, f"Likelihoods_time{ext}"), transparent=False)
        fig1.savefig(os.path.join(save_path, f"Likelihoods_dist{ext}"), transparent=False)
        fig2.savefig(os.path.join(save_path, f"XY_pos_time{ext}"), transparent=False)

    if view == 'sideview':
        print("Investigating tongue and jaw")
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.scatter(np.where(data['jaw']['likelihood'] > 0.6, data['jaw']['y'], 0),
                   np.where(data['tongue']['likelihood'] > 0.6, data['tongue']['y'], 0), s=5, c='k', alpha=0.5)
        ax.set_xlabel('jaw vertical')
        ax.set_ylabel('tongue vertical')
        for ext in [".png", ".svg"]:
            fig.savefig(os.path.join(save_path, f"tongue_jaw_corr{ext}"), transparent=False)

    plot_aligned = [['tongue', 'jaw'] if view == 'sideview' else ['whisker_tip']][0]

    for part in plot_aligned:
        peaks, _ = find_peaks(np.where(data[part]['likelihood'] > 0.6, data[part]['y'], 0), distance=500)

        fig, ax = plt.subplots()
        for peak in peaks:
            if (peak-250) < 0 or (peak+250) > data.shape[0]:
                continue

            trace = np.where(data[part]['likelihood'] > 0.6, data[part]['y'], np.nan)[(peak - 250):(peak + 250)]
            if trace.shape[0] == 0:
                trace = np.zeros(500)

            ax.plot(range(500), trace)

        for ext in [".png", ".svg"]:
            fig.savefig(os.path.join(save_path, f"{part}_peak_aligned{ext}"), transparent=False)

    colors = cm.rainbow(np.linspace(0, 1, len(bodyparts)))

    for part in parts_to_make_clips:
        peaks, _ = find_peaks(np.where(data[part]['likelihood'] > 0.6, data[part]['y'], 0), distance=500,
                              threshold=np.where(data[part]['likelihood'] > 0.6, data[part]['y'], 0).std()*1.8)
        peaks = [43170]
        if len(peaks) == 0:
            peaks, _ = find_peaks(np.where(data[part]['likelihood'] > 0.6, data[part]['y'], 0), distance=500)

        if len(peaks) > 0 and len(peaks) < 5:
            sample_peaks = peaks

        elif len(peaks) >= 5:
            sample_peaks = sample(peaks, 5)

        else:
            print(f"No peaks found for  {part}, skipping videos")
            continue

        if make_video == False:
            continue

        for peak in sample_peaks:
            if (peak-500) < 0 or (peak+500) > data.shape[0]:
                peak = sample(peaks.tolist(), 1)[0]

            im_stack = []
            print("Generating videos of 10 tongue events")
            video.set(cv2.CAP_PROP_POS_FRAMES, peak-500)
            for i in tqdm(range(1000)):
                ret, frame = video.read()
                fig, ax = plt.subplots()
                ax.imshow(frame, aspect='auto')
                for part, color in zip(bodyparts, colors):
                    ax.scatter(data[part]['x'][peak - 500 + i], data[part]['y'][peak - 500 + i], s=50,
                               c=color.reshape(1,-1), label=part,
                               marker='o' if data[part]['likelihood'][peak - 500 + i] > 0.6 else 'x')
                ax.set_xlim(0, frame.shape[1])
                ax.set_ylim(frame.shape[0], 0)
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
                fig.legend(fontsize="x-small")
                fig.savefig(os.path.join(save_path, 'temp', f'labelled_frame_{i}.jpeg'))
                fig.clear()
                im_stack += [np.asarray(
                    Image.open(os.path.join(save_path, 'temp', f'labelled_frame_{i}.jpeg').replace("\\", "/")))]
                os.remove(os.path.join(save_path, 'temp', f'labelled_frame_{i}.jpeg').replace("\\", "/"))

            print(f"Obtained labelled image stack, len before = {len(im_stack)}, len after stack {np.stack(im_stack, axis=0).shape}")
            im_stack = np.stack(im_stack, axis=0)
            print("Writting video, next")
            tifffile.imwrite(os.path.join(save_path, f"{vid.split('/')[-2]}_{part}_video_frame_{peak-500}-{peak+500}.tif"), im_stack)

    return 0


if __name__ == "__main__":

    user = "Pol_Bech"
    json_name = "topview_dlc_config_RD.json"
    view = json_name.split("_")[0]
    server_path = "//sv-nas1.rcp.epfl.ch/Petersen-Lab"

    json_path = os.path.join(fr"C:\Users\bechvila\Desktop\Python_repo", "LSENS-DeepLabCut", "json_files", json_name)
    with open(json_path, "r") as f:
        json_config = json.load(f)

    count = 0
    for i, (vid_file, dest_folder) in enumerate(zip(json_config['videos_to_anly'], json_config['server_dest_folder'])):
        # if vid_file.split("/")[-2] not in ["RD039_20240222_145509", "RD039_20240228_182245", "RD043_20240229_145751", "RD043_20240301_104556",
        #                                    "RD043_20240306_175640", "RD045_20240227_183215", "RD045_20240228_171641", "RD045_20240229_172110",
        #                                    "RD045_20240301_141157"]:
        #     continue
        # else:
        #     count += 1
        #
        # if i < 18:
        #     continue
        if "RD042" not in vid_file:
            continue
        dest_file = os.path.join(server_path, dest_folder, view).replace("\\", "/")
        dlc_file = [file for file in os.listdir(dest_file) if ".csv" in file]
        dlc_file = [file for file in dlc_file if view in file]

        if len(dlc_file) == 0:
            print(f"No dlc data for session {vid_file.split('/')[-2]}")
            continue

        vid = os.path.join(server_path, vid_file).replace("\\", "/")

        check_dlc(vid=vid,
                  file=os.path.join(server_path, dest_folder, json_name.split("_")[0], dlc_file[0]).replace("\\", "/"),
                  view=json_name.split("_")[0],
                  parts_to_make_clips=["tongue" if "side" in json_name else "whisker_tip"])
