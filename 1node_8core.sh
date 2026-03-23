#!/bin/bash
#SBATCH --job-name=lang_1n8c
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --output=out_1node_8core.txt

module load Python
module load mpi4py

mpirun -np 8 python lang_count_mpi.py mastodon-large.ndjson bluesky-large.ndjson