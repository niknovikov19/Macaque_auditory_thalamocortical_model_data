from netpyne.batchtools.search import search
import numpy as np


def generate_freqs(f0, fn, df_mult, n):
    # Generate n freqs from f0 to fn, with df changing from 1 to df_mult
    df = np.linspace(1, df_mult, n)
    f = np.cumsum(df) - 1
    f = f0 + f * (fn - f0) / f[-1]
    return f

params = {'osc_f': generate_freqs(3, 50, 3, 25),
          'osc_pop_name': ['IT3']}

sge_config = {
    'queue': 'cpu.q',
    'cores': 50,
    'vmem': '128G',
    'realtime': '1:30:00',
    'command': ('conda activate netpyne_batch \n'
                'export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH \n'    
                'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init.py')
    }

search(job_type = 'sge',
       comm_type = 'socket',
       label = 'grid',
       params = params,
       output_path = '../grid_batch_5sec_IT3_IT5A_IT5B',
       checkpoint_path = '../ray',
       run_config = sge_config,
       num_samples = 1,
       max_concurrent = 9)
