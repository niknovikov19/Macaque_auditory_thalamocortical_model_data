import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

from neuron import h
try:
    h.nrn_load_dll(r'..\nrnmech.dll')
except:
    pass

#from netpyne.batchtools import comm, specs
from netpyne import sim, specs


# Load config that corresponds to Fig. 4A
fpath_cfg = 'v34_batch56_0_0_cfg.json'
with open(fpath_cfg, 'r') as fid:
    cfg_dict = json.load(fid)
cfg = specs.SimConfig(cfg_dict['simConfig'])

# TEST: single-cell populations
cfg.singleCellPops = 1

# =============================================================================

with open('netParams_sub.json', 'r') as fid:
    netParams_sub = json.load(fid)['net']['params']

# Prepare simulation
sim.initialize(simConfig=cfg, netParams=netParams_sub)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.addStims() 							        # add network stimulation
sim.net.connectCells()            			# create connections between cells based on params
