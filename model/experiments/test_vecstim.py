import json

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

from netpyne import sim, specs


fpath_cfg = '/ddn/niknovikov19/repo/A1_model_old/model/v34_batch56_0_0_cfg.json'
fpath_par = ('/ddn/niknovikov19/repo/A1_model_old/data/exp_subnet_L3_8s_replay_t=1-10'
             '/exp_subnet_L3_8s_replay_t=1-10_netParams_sub.json')

with open(fpath_cfg, 'r') as fid:
    cfg_dict = json.load(fid)
cfg = specs.SimConfig(cfg_dict['simConfig'])

with open(fpath_par, 'r') as fid:
    netParams_sub = json.load(fid)
netParams_sub = specs.NetParams(netParams_sub['net']['params'])

cfg.singleCellPops = 0

# Prepare simulation
sim.initialize(simConfig=cfg, netParams=netParams_sub)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
