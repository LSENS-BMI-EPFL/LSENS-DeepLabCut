#!/bin/bash -l
#SBATCH --job-name=train_dlc
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --partition h100
#SBATCH --time=24:00:00
#SBATCH --output=/home/%u/logs/%j.out
#SBATCH --error=/home/%u/logs/%j.err
#SBATCH --mail-user=pol.bechvilaseca@epfl.ch
#SBATCH --mail-type=END,FAIL
module load gcc openmpi cudnn 
source /home/${USER}/venvs/DLC3.0/bin/activate
cd /home/${USER}/LSENS-DeepLabCut
config_path = /home/bechvila/context_top_dlc-PB-2025-01-09/config.yaml
echo "Training network in $config_path"
python train_DLC_network.py config_path
