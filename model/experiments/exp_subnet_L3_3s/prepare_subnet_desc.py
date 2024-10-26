import numpy as np
from pathlib import Path
import sys

from netpyne.batchtools import specs #import SimConfig

sys.path.append(str(Path(__file__).resolve().parents[3]))
from subnet_tuner import SubnetDesc


def prepare_subnet_desc(pop_rate_data: dict, cfg: specs.SimConfig) -> SubnetDesc:    
    desc = SubnetDesc()
    #desc.pops_active = ['IT3', 'SOM3', 'PV3', 'VIP3', 'NGF3']
    desc.pops_active = cfg.subnet_par['pops_active']
    desc.conns_frozen = []
    for pop in pop_rate_data:
        if pop not in desc.pops_active:
            desc.inp_surrogates[pop] = {
                'type': 'irregular',
                'rate': np.mean(pop_rate_data[pop]),
                'noise': 1.0
                }
    return desc

