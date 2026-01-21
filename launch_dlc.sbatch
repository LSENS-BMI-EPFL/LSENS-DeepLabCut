#!/bin/bash -l
#SBATCH --job-name=PB_dlc
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --cpus-per-task 2
#SBATCH --mem=0
#SBATCH --partition h100
#SBATCH --time 3-0
#SBATCH --mail-type=END,FAIL
#SBATCH --error=/home/%u/logs/%j.err
#SBATCH --output=/home/%u/logs/%j.out
#SBATCH --mail-user=%u

module load gcc openmpi cudnn ffmpeg 
source /home/${USER}/venvs/DLC3.0/bin/activate
cd /home/${USER}/LSENS-DeepLabCut

echo "INFO: Running DLC with arguments: $@"
python run_DLC.py $@