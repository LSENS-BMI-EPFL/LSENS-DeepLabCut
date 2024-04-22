# LSENS-DeepLabCut
LSENS repository for deeplabcut models and preprocessing scripts
Get access: Talk to Carl
Set up cluster:
1.	Open Anaconda Prompt. Type: ssh <gaspar id>@<cluster>.epfl.ch
a.	Cluster can be izar, jed, or helvetios for scitas clusters
b.	You’ll be prompted to type your password
2.	You will be dropped in your /home folder. This is to have “permanent” files with info or .sbatch files for running your routines.
3.	Mount LSENS server:
a.	Create server folder -> type: mkdir servers
b.	Type: vim .bashrc
c.	Press i to be able to edit
d.	In the last line copy paste (paste in command line is done by right clicking):
gio mount smb://intranet\;<gaspar_id> @sv-nas1.rcp.epfl.ch/Petersen-lab
ln -s  /run/user/$(id -u)/gvfs/smb-share\:domain\=intranet\,server\=sv-nas1.rcp.epfl.ch\,share\=petersen-lab\,user\=<gaspar_id>/* ~/servers
e.	Press ESC and then type “:wq” to save and quit (you can use just “:q” to quit without saving)
4.	Load necessary modules: 
a.	Type: module load gcc python openmpi py-tensorflow
5.	Create virtual environment:
a.	Type: mkdir venvs
b.	Type: virtualenv --system-site-packages venvs/DLC
6.	Activate DLC virtualenv and install deeplabcut:
a.	Type: source venvs/DLC/bin/activate
b.	python -m pip install --no-cache-dir deeplabcut==2.3.9
c.	python -m pip install --no-cache-dir typing-extensions==4.6
d.	python -m pip install --no-cache-dir keras==2.10
7.	Test DLC installation
a.	Python
b.	Import deeplabcut
8.	Set up file transfer: 
a.	Install WinSCP in your local computer
b.	Create folder in your /home/<gaspar_id> directory for the files you want to run: you will need a folder with your code (i.e this repo), and a logs folder.
c.  Create folder in your /scratch/izar/<gaspar_id> directory for the videos (videos_to_anly) and for the results (dlc_results). Copy your network on the scratch folder too.

To train your network:
1. Create and label your project in your local computer (no gpu needed but make sure the deeplabcut version is the same).
2. Change the path in your config.yaml to the correct cluster path and transfer your network to the cluster.
3. In terminal:
a. source venvs/DLC/bin/activate
b. Open a python instance typing python and import deeplabcut. Pointing the network to your config path (somehting like /scratch/izar/<gaspar_id>/<yournetworkname>/config.yaml), create training dataset: dlc.create_training_dataset(config_path). This is important to do already on the cluster since otherwise you will have path issues. Close python.
c. Edit the train.sbatch file in the repo with the path to your network config.yaml file. You can type in terminal: vim /home/<gaspar_id>/LSENS-DeepLabCut/train.sbatch, press "i" to insert and change the name of the job, the max time of the job (12 h should be more than enough) and the email so you receive notifications if your code finishes or crashes. Exit vim by pressing ESC, typing :wq to save or :q! to not save 
d. Run your training by typing in terminal sbatch train.sbatch

To analyze videos:
1. Create a .json file with the make_json_config.py file. You can do this on your local computer. Note that you may have to tweak a few parameters like your config_path (in cluster).
2. Copy the json file to the json_files folder in your server.
3. Activate environment: source venvs/DLC/bin/activate
4. Run analysis: python /home/$(whoami)/LSENS-DeepLabCut/data_transfer_and_run.py $(whoami) <name of json file>
5. After everything ran, transfer data and delete videos from scratch folder by using the command: python /home/$(whoami)/LSENS-DeepLabCut/transfer_results.py $(whoami) <name of json file>

Enjoy and may the pose estimation gods be with you!
