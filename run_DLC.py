import os
import sys
import json
import timeit
import shutil
import deeplabcut as dlc
from deeplabcut.utils.auxfun_videos import VideoWriter


def run_dlc_anly():
	print(sys.argv)
	config_path = sys.argv[1]
	video_path = sys.argv[2]
	dest_path = sys.argv[3]

	video_name = video_path.split("/")[-1][:-4]
	user = video_path.split("/")[3]

	if not os.path.exists(config_path):
		ValueError("DLC config.yaml not found")
		return 1

	if not os.path.exists(video_path):
		print('video not copied')
		return 1
	
	if not os.path.exists(os.path.join(dest_path, 'split_videos')):
		os.makedirs(os.path.join(dest_path, 'split_videos'))

	vid = VideoWriter(video_path)
	clips = vid.split(n_splits=10, dest_folder=os.path.join(dest_path, 'split_videos'))

	start = timeit.default_timer()
	dlc.analyze_videos(config_path, os.path.join(dest_path, 'split_videos'), videotype=video_path.split('/')[-1][-4:], save_as_csv=True, destfolder=dest_path)
	end = timeit.default_timer()
	
	print(f"DLC ran without issues in {round((end-start)/60, 2)} min")
	dlc.filterpredictions(config_path, os.path.join(dest_path, 'split_videos'), videotype=video_path.split('/')[-1][-4:], save_as_csv=True, destfolder=dest_path)
	dlc.plot_trajectories(config_path, os.path.join(dest_path, 'split_videos'), videotype=video_path.split('/')[-1][-4:], filtered=True, destfolder=dest_path)
	
if __name__ == "__main__":
	run_dlc_anly()