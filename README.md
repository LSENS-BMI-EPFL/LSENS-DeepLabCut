# LSENS-DeepLabCut
LSENS repository for deeplabcut model training in SCITAS clusters and preprocessing scripts
Get SCITAS access: Talk to Carl
Set up cluster:
1.	Open Anaconda Prompt. Type: `ssh <gaspar id>@<cluster>.hpc.epfl.ch`
- Cluster has to be Kuma for DLC, as it is the only one with GPUs
- You’ll be prompted to type your gaspar password
- You will be dropped in your /home folder. This is to have “permanent” files with info or .sbatch files for running your routines.
2.	Mount LSENS server:

Create servers folder -> type: 
```
mkdir servers
```
Open bashrc file: 
```
vim .bashrc
```
Press _i_ to be able to edit bashrc file
In the last line of the bashrc file copy paste (paste in command line is done by right clicking):

```
gio mount smb://intranet\;<gaspar_id>@sv-nas1.rcp.epfl.ch/Petersen-lab
ln -s  /run/user/$(id -u)/gvfs/smb-share\:domain\=intranet\,server\=sv-nas1.rcp.epfl.ch\,share\=petersen-lab\,user\=<gaspar_id>/* ~/servers
```

and replace `<gaspar_id>` appropriately.

Press ESC and then type “:wq” to save and quit (you can use just “:q” to quit without saving)

3.	Load necessary modules: 
Type: 
```
module load gcc openmpi py-tensorflow
```
4.	Create virtual environment:
Type:
```
mkdir venvs
python -m venv ./venvs/DLC
```
5.	Activate DLC virtualenv and install deeplabcut:
From kuma_environment.txt:
```
pip install -r kuma_environment.txt
```

Check python version == 3.11
Type:
```
python -V
```

Type:
```
source venvs/DLC/bin/activate
python -m pip install --no-cache-dir deeplabcut==3.0.0rc6
python -m pip install --no-cache-dir typing-extensions==4.12.2
```

6.	Test DLC installation
  a.	In command line open python: type: `python`, then
```
import deeplabcut
```

7.	Set up file transfer: 
a.	Install WinSCP in your local computer
b.	Create folder in your /home/<gaspar_id> directory for the files you want to run: you will need a folder with your code (i.e this repo), and a logs folder.
c.  Create folder in your /scratch/izar/<gaspar_id> directory for the videos (videos_to_anly) and for the results (dlc_results). Copy your network on the scratch folder too.

To train your network:
1. Create and label your project in your local computer (no gpu needed but make sure the deeplabcut version is the same).
2. Change the path in your config.yaml to the correct cluster path and transfer your network to the cluster.
3. In terminal:
```
source venvs/DLC/bin/activate
```
  a. Open a python instance typing python and import deeplabcut. Pointing the network to your config path (somehting like /scratch/izar/<gaspar_id>/<yournetworkname>/config.yaml), create training dataset: dlc.create_training_dataset(config_path). This is important to do  already on the cluster since otherwise you will have path issues. Close python.
  b. Edit the train.sbatch file in the repo with the path to your network config.yaml file. You can type in terminal: vim /home/<gaspar_id>/LSENS-DeepLabCut/train.sbatch, press "i" to insert and change the name of the job, the max time of the job (12 h should be more     than enough) and the email so you receive notifications if your code finishes or crashes. Exit vim by pressing ESC, typing :wq to save or :q! to not save 
  c. Run your training by typing in terminal:
```
sbatch train.sbatch
```
To analyze videos:
1. Create a .json file with the make_json_config.py file. You can do this on your local computer. Note that you may have to tweak a few parameters like your config_path (in cluster).
2. Copy the json file to the json_files folder in your server.
3. Activate environment:
```
source venvs/DLC/bin/activate
```
5. Run analysis:
```
python /home/$(whoami)/LSENS-DeepLabCut/data_transfer_and_run.py $(whoami) <name of json file>
```
6. After everything ran, transfer data and delete videos from scratch folder by using the command:
```
python /home/$(whoami)/LSENS-DeepLabCut/transfer_results.py $(whoami) <name of json file>
```

Enjoy and may the pose estimation gods be with you!



#### Troubleshooting tips
- When installing DLC in your virtual env, you get the following error: `TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'` This means you have to either downgrade or upgrade the `packaging` module e.g. >22.0 or higher.


