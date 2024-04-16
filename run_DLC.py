import os
import sys
import json
import timeit
import shutil
import deeplabcut as dlc

def run_dlc_anly():

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

	start = timeit.default_timer()
	dlc.analyze_videos(config_path, [video_path], videotype="avi", save_as_csv=True, destfolder=dest_path)
	end = timeit.default_timer()
	print(f"DLC ran without issues in {round((end-start)/60, 2)} min")

if __name__ == "__main__":
	run_dlc_anly()