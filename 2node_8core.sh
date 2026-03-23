#!/bin/bash
#SBATCH --job-name=lang_2n8c
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=out_2node_8core.txt

module load Python
module load mpi4py

mpirun -np 8 python lang_count_mpi.py mastodon-large.ndjson bluesky-large.ndjson