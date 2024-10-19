#!/bin/bash
#$ -cwd
#$ -N A1_single
#$ -q cpu.q
#$ -pe smp 60
#$ -l h_vmem=256G
#$ -l h_rt=6:00:00
#$ -o /ddn/niknovikov19/repo/A1_model_old/log/A1_single_log.txt
#$ -e /ddn/niknovikov19/repo/A1_model_old/log/A1_single_err.txt

source ~/.bashrc
#echo $(pwd)
conda activate netpyne_batch
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
cd /ddn/niknovikov19/repo/A1_model_old/model
mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi experiments/init_single.py