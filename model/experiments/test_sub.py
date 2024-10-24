import importlib.util
import json
from pathlib import Path
import pickle as pkl
import sys

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

#from netpyne.batchtools import comm, specs
from netpyne import sim, specs

sys.path.append(str(Path(__file__).resolve().parents[2]))

from subnet_tuner import SubnetDesc, SubnetParamBuilder

from create_base_cfg_v34_batch56 import create_base_cfg
from create_net_params import create_net_params


def _load_module(fpath_mod):
    mod_spec = importlib.util.spec_from_file_location(
        'module.name', fpath_mod)
    mod = importlib.util.module_from_spec(mod_spec)
    sys.modules['module.name'] = mod
    mod_spec.loader.exec_module(mod)
    return mod


exp_name = 'exp_subnet_L3_3s'

# Import experiment-specific config py-file
dirpath_exp = Path(__file__).resolve().parent / exp_name
fpath_exp_cfg = dirpath_exp / 'exp_cfg.py'
cfg_mod = _load_module(fpath_exp_cfg)

# Import experiment-specific py-file with subnet description
fpath_exp_subnet = dirpath_exp / 'prepare_subnet_desc.py'
subnet_mod = _load_module(fpath_exp_subnet)

# Initialize config object, common for every experiment of the model
cfg = create_base_cfg()

# Apply experiment-specific config modifications
cfg_mod.apply_exp_cfg(cfg)

# Automatically set the experiment name in config
cfg.simLabel = exp_name
dirpath_data = Path(__file__).resolve().parents[2] / 'data'
dirpath_exp = dirpath_data / exp_name
cfg.saveFolder = str(dirpath_exp)

# Update config by batchtools
cfg.update_cfg()

# TEST: single-cell populations
cfg.singleCellPops = 1

# Create netParams of the full model based on the config
netParams_full = create_net_params(cfg)

# Load firing rate data from a previous simulation for subnet builder
fpath_rates = str(dirpath_data / 'A1_paper' / 'v34_batch56_10s_pop_rates.pkl')
with open(fpath_rates, 'rb') as fid:
    pop_rate_data = pkl.load(fid)

# Create subnet netParams
desc = subnet_mod.prepare_subnet_desc(pop_rate_data)
spb = SubnetParamBuilder()    
netParams_sub = spb.build(netParams_full.todict(), desc)
netParams_sub = specs.NetParams(netParams_sub)

cfg.save(str(dirpath_exp / f'{exp_name}_cfg.json'))
netParams_full.save(str(dirpath_exp / f'{exp_name}_netParams_full.json'))
netParams_sub.save(str(dirpath_exp / f'{exp_name}_netParams_sub.json'))

# Prepare simulation
sim.initialize(simConfig=cfg, netParams=netParams_sub)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							        # add network stimulation
