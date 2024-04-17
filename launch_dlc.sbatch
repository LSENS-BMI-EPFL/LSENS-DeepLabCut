#!/bin/bash -l
#SBATCH --job-name=RD_dlc
#SBATCH --nodes=1
#SBATCH --time 3-0
#SBATCH --gres=gpu:1
#SBATCH --mail-type=END,FAIL
#SBATCH --error=/home/%u/logs/%j.err
#SBATCH --output=/home/%u/logs/%j.out
#SBATCH --mail-user=pol.bechvilaseca@epfl.ch

module load gcc python openmpi py-tensorflow
source /home/${USER}/venvs/DLC/bin/activate
cd /home/${USER}/LSENS-DeepLabCut

echo "INFO: Running DLC with arguments: $@"
python run_DLC.py $@