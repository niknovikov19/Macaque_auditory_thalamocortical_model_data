#!/bin/bash
#$ -cwd
#$ -N A1_run_10um_5s_256G
#$ -q cpu.q
#$ -pe smp 50
#$ -l h_vmem=256G
#$ -l h_rt=2:00:00
#$ -o /ddn/niknovikov19/repo/A1_model_old/log/A1_run_IT3_w_10_6_log.txt
#$ -e /ddn/niknovikov19/repo/A1_model_old/log/A1_run_IT3_w_10_6_err.txt

source ~/.bashrc
#echo $(pwd)
conda activate netpyne_batch
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
cd /ddn/niknovikov19/repo/A1_model_old/model/
mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py