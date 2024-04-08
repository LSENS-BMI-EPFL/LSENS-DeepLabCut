#!/bin/bash -l
#SBATCH --job-name=PB_dlc
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
videos='PB175_20240311_170817_sideview'
echo "Analyzing videos ${videos}"
python run_DLC.py videos
