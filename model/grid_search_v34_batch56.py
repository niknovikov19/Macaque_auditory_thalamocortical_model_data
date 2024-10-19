from netpyne.batchtools.search import search
import numpy as np


#params = {'EbkgThalamicGain': np.linspace(2, 6, 8)}
#params = {'TC_leak_mult': [0., 0.0001, 0.001]}
#params = {'TC_ebkg_mult': [0.7, 0.85, 1., 1.15, 1.3]}
#params = {'IRE_ibkg_mult': [3., 4., 5., 6.]}
#params = {'osc_f': [15, 60],
#          'osc_pop_name': ['IT2', 'IT3', 'ITP4', 'IT5A', 'IT5B', 'IT6']}
#params = {'osc_f': [15],
#          'osc_pop_name': ['IT3', 'IT5A', 'IT6']}

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
    'cores': 60,
    'vmem': '256G',
    'realtime': '2:30:00',
    'command': ('conda activate netpyne_batch \n'
                'export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH \n'    
                'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi init_v34_batch56.py')
    }

search(job_type = 'sge',
       comm_type = 'socket',
       label = 'grid',
       params = params,
       output_path = '../data/grid_batch_v34_batch56_IT3osc_repbkg',
       checkpoint_path = '../ray',
       run_config = sge_config,
       num_samples = 1,
       max_concurrent = 13)
