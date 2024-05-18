#!/bin/bash -l
#SBATCH --job-name=train_dlc
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00
#SBATCH --output=/home/%u/logs/%j.out
#SBATCH --error=/home/%u/logs/%j.err
#SBATCH --mail-user=pol.bechvilaseca@epfl.ch
#SBATCH --mail-type=END,FAIL
module load gcc python openmpi py-tensorflow
source /home/${USER}/venvs/DLC/bin/activate
cd /home/${USER}/LSENS-DeepLabCut
config_path = /scratch/izar/bechvila/context_dlc_topview-PB-2024-02-21/config.yaml
echo "Training network in $config_path"
python train_DLC_network.py config_path
