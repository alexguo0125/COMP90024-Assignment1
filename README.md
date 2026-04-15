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
