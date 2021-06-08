#!/bin/bash
#SBATCH --time=07:00:00
#SBATCH --mem=10G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
source /nfs/user/gs289biny/new_train/test/env/bin/activate
python3.4  /nfs/user/gs289biny/new_train/400/train_400.py
python3.4  /nfs/user/gs289biny/new_train/400/SignatureDetector.py
deactivate
