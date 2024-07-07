from netpyne.batchtools.search import search
import numpy as np


params = {'EbkgThalamicGain', [2, 4, 6, 8, 10, 12, 14, 16]}

sge_config = {
    'queue': 'cpu.q',
    'cores': 60,
    'vmem': '256G',
    'realtime': '1:30:00',
    'command': ('conda activate netpyne_batch \n'
                'export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH \n'    
                'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init_v34_batch56.py')
    }

search(job_type = 'sge',
       comm_type = 'socket',
       label = 'grid',
       params = params,
       output_path = '../grid_batch_v34_batch56',
       checkpoint_path = '../ray',
       run_config = sge_config,
       num_samples = 1,
       max_concurrent = 13)
