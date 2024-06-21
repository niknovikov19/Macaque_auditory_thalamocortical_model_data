from netpyne.batchtools.search import search
import numpy as np

params = {'osc_f': [5, 10, 15, 20]}

sge_config = {
    'queue': 'cpu.q',
    'cores': 15,
    'vmem': '64G',
    'realtime': '1:30:00',
    'command': ('conda activate netpyne3 \n'
                'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py')
    }

search(job_type = 'sge',
       comm_type = 'socket',
       label = 'grid',
       params = params,
       output_path = '../grid_batch',
       checkpoint_path = '../ray',
       run_config = sge_config,
       num_samples = 1,
       max_concurrent = 9)
