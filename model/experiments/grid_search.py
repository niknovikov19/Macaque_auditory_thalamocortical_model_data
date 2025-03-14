import importlib.util
from pathlib import Path
import sys

from netpyne.batchtools.search import search
import numpy as np


def _load_module(fpath_mod):
    mod_spec = importlib.util.spec_from_file_location(
        'module.name', fpath_mod)
    mod = importlib.util.module_from_spec(mod_spec)
    sys.modules['module.name'] = mod
    mod_spec.loader.exec_module(mod)
    return mod


exp_name = 'exp_batch_subnet_L3_wrec_wxe_6x6_poiss_8s'

# Import experiment-specific batch_params.py and get batch params
dirpath_exp = Path(__file__).resolve().parent / exp_name
fpath_batch_params = dirpath_exp / 'batch_params.py'
batch_params_mod = _load_module(fpath_batch_params)
params = batch_params_mod.get_batch_params()

sge_config = {
    'queue': 'cpu.q',
    'cores': 30,
    'vmem': '128G',
    'realtime': '3:30:00',
    'command': ('conda activate netpyne_batch \n'
                'export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH \n'
                'cd .. \n'
                'mpiexec -n $NSLOTS -hosts $(hostname) nrniv -python -mpi experiments/init_sub_batch.py')
    }

search(job_type = 'sge',
       comm_type = 'socket',
       label = exp_name,
       params = params,
       output_path = f'../data/{exp_name}',
       checkpoint_path = '../ray',
       run_config = sge_config,
       num_samples = 1,
       max_concurrent = 25)
