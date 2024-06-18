#!/bin/bash
#$ -cwd
#$ -N A1_run_5sec
#$ -q cpu.q
#$ -pe smp 15
#$ -l h_vmem=16G
#$ -l h_rt=4:00:00
#$ -o /ddn/niknovikov19/repo/A1_model_old/log/A1_run_5sec_log.txt
#$ -e /ddn/niknovikov19/repo/A1_model_old/log/A1_run_5sec_err.txt

source ~/.bashrc
#echo $(pwd)
conda activate netpyne3
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
cd /ddn/niknovikov19/repo/A1_model_old/model/
mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py