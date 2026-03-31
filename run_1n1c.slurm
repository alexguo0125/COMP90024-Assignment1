#!/bin/bash
#SBATCH --job-name=run_1n1c
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mail-user=mgifari@student.unimelb.edu.au
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --time=0-01:00:00
#SBATCH --partition=sapphire
#SBATCH --output=out_1node_1core.txt

# check that the script is launched with sbatch
if [ "x$SLURM_JOB_ID" == "x" ]; then
   echo "You need to submit your job to the queuing system with sbatch"
   exit 1
fi

# Run the job from the directory where it was launched (default)

module load mpi4py/3.1.4-Python-3.11.3

mpiexec -n 1 python langcounter_mpi.py