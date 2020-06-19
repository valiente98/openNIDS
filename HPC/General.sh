#!/bin/bash

#Created by valiente98 on 2020.

# SCRIPT NAME: General.sh

#SBATCH -J General

# Partition type
#SBATCH --partition=medium

# Number of nodes
#SBATCH --nodes=1

# Number of tasks
#SBATCH --ntasks=1

# Number of task per node
#SBATCH --tasks-per-node=1

# Memory per node
#SBATCH --mem=50g

# Number of GPUs per node
#SBATCH --gres=gpu:1

# Working directory
#SBATCH --workdir=/homedtic/jvaliente/IDS-TFG

# Output
#SBATCH -o %J.out

# Error
#SBATCH -e %J.err

#Modules
module load scikit-learn
module load matplotlib

python3 rfGeneral.py
