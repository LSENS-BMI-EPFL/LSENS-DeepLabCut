#!/bin/bash -l
#SBATCH --job-name=RD_dlc
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time 3-0
#SBATCH --output=/home/%u/logs/%j.out
#SBATCH --error=/home/%u/logs/%j.err
#SBATCH --mail-user=pol.bechvilaseca@epfl.ch
#SBATCH --mail-type=END,FAIL

module load gcc python openmpi py-tensorflow
source /home/${USER}/venvs/DLC/bin/activate
cd /home/${USER}/LSENS-DeepLabCut

jsonfile="/home/bechvila/LSENS-DeepLabCut/json_files/sideview_dlc_config_RD.json"

config=$(python -c "import json; print(json.load(open('$jsonfile'))['config_path'])")
vid_to_anly=$(python -c "import json; print(json.load(open('$jsonfile'))['videos_to_anly'][0])")
serv_dest_folder=$(python -c "import json; print(json.load(open('$jsonfile'))['server_dest_folder'][0])")
dest_folder="/scratch/izar/${USER}/videos_to_anly"
server_path="/home/${USER}/servers"
result_folder="/scratch/izar/${USER}/dlc_results"

stripped_variable=${vid_to_anly//[\"\[\]]/}
IFS=',' read -ra strings <<< "$stripped_variable"
num_strings=${#strings[@]}

for ((i=0; i<"$num_strings"; i++)); do
    video_path=$(python -c "import json; print(json.load(open('$jsonfile'))['videos_to_anly'][$i])")
    anly_folder=$(python -c "import json; print(json.load(open('$jsonfile'))['server_dest_folder'][$i])")
    video_name=$(echo "$video_path" | awk -F'/' '{print $NF}')
    # Print the current variables
    echo "Copying file: $video_name"
    scp "${server_path}/${video_path}" "${dest_folder}"
    
    echo "File copied, analyzing video data"
    # Run the Python script with the variables as arguments
    python run_DLC.py "$config" "${dest_folder}/${video_name}"
    
    echo "DLC analysis finished. Transferring data and cleanup."
    for file in "${result_folder}/${video_name}"/*; do
        if [ -f "$file" ]; then
            # Use scp to copy the file to the destination folder
            scp "$file" "${server_path}/${serv_dest_folder}"
            # If using scp across different machines, you might need to provide password or set up SSH keys for passwordless authentication
        fi
    done
    rm -f "${dest_folder}/${video_name}"
done
