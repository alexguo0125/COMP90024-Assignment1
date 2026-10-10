# COMP90024 Assignment 1

This repository contains the implementation and results for **COMP90024 Cluster and Cloud Computing Assignment 1**.

## Overview

The project focuses on analysing large-scale **Mastodon** and **BlueSky** datasets in **NDJSON format** using the **Spartan HPC system**.  
The main objective is to count language usage and evaluate the performance of different parallelisation strategies using MPI.

Two approaches were implemented and compared:

- Modulo-based parallelisation
- Byte-chunking parallelisation

The final implementation uses byte-chunking, which achieved better runtime performance.

---

## Repository Structure

### Core Scripts

- `langcounter.py`  
  Baseline language counting implementation.

- `pdlangcounter.py`  
  Pandas-based version used for initial testing.

- `v1_langcounter_mpi.py`  
  Initial MPI implementation.

- `v2_langcounter_mpi.py`  
  Improved MPI version with optimisations.

- `v3_langcounter_mpi.py`  
  Final MPI implementation using byte-chunking.

- `checkdata.py`  
  Script used to inspect dataset structure.

---

### SLURM Scripts (Spartan HPC)

- `run_1n1c.slurm` → 1 node, 1 core  
- `run_1n8c.slurm` → 1 node, 8 cores  
- `run_2n8c.slurm` → 2 nodes, 8 cores  

---

### Output Files

- `out1/`  
  Output results for modulo-based method

- `out2/`  
  Output results for byte-chunking method

Each output includes:
- Top-10 language counts
- Number of "No language" records
- Number of "Bad JSON" records
- Runtime for each configuration

---

### Dependencies

- Python 3
- mpi4py
- pandas (for baseline testing)

Install dependencies:

```bash
pip install -r requirements.txt
```

The baseline scripts expect NDJSON inputs under `datasets/`. Update the input
paths near the top of the selected script if your files are stored elsewhere,
then run, for example:

```bash
python langcounter.py
```

The MPI variants and SLURM launch scripts are intended for the University of
Melbourne Spartan environment. Dataset files are not included in this
repository.

## Key Insights

- Byte-chunking significantly reduces redundant file reading compared to modulo-based distribution
- 1 node 8 cores achieved optimal performance due to shared-memory advantages
- Distributed execution (2 nodes) introduces communication overhead that limits scalability
- The results align with Amdahl’s Law, showing diminishing returns as parallelism increases

## Notes

This is an academic project for COMP90024 Cluster and Cloud Computing. The
repository preserves the implementation, benchmark launch scripts, and output
summaries so the parallelisation choices can be inspected and reproduced with
equivalent input data.
