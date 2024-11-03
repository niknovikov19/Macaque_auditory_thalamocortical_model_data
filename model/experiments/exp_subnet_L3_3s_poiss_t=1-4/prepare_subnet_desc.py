import numpy as np
from pathlib import Path
import sys

from netpyne.batchtools import specs #import SimConfig

sys.path.append(str(Path(__file__).resolve().parents[3]))
from subnet_tuner import SubnetDesc


def prepare_subnet_desc(sim_data: dict, cfg: specs.SimConfig) -> SubnetDesc:    
    desc = SubnetDesc()
    desc.pops_active = cfg.subnet_par['pops_active']
    desc.conns_frozen = []
    
    if cfg.subnet_par['inp_type'] == 'poisson':
        for pop, rr in sim_data['rates'].items():
            if pop not in desc.pops_active:
                desc.inp_surrogates[pop] = {
                    'type': 'irregular',
                    'rate': np.mean(rr),
                    'noise': 1.0
                    }
    elif cfg.subnet_par['inp_type'] == 'spike_replay':
        for pop, spikes in sim_data['spikes'].items():
            if pop not in desc.pops_active:
                desc.inp_surrogates[pop] = {
                    'type': 'spike_replay',
                    'spkTimes': spikes
                    }
                    
    return desc

