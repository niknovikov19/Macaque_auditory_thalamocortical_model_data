import importlib.util
import json
import os
from pathlib import Path
import pickle as pkl
import sys

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

from netpyne.batchtools import comm #, specs
from netpyne import sim, specs

sys.path.append(str(Path(__file__).resolve().parents[2]))

from subnet_tuner import SubnetDesc, SubnetParamBuilder
import subnet_tuner.sim_res_parse_utils as srp

from create_base_cfg_v34_batch56 import create_base_cfg
from create_net_params import create_net_params


#exp_name = 'test_run_1'
#is_batch = False


def _load_module(fpath_mod):
    mod_spec = importlib.util.spec_from_file_location(
        'module.name', fpath_mod)
    mod = importlib.util.module_from_spec(mod_spec)
    sys.modules['module.name'] = mod
    mod_spec.loader.exec_module(mod)
    return mod


def run_exp(exp_name, is_batch):
    
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
    
    # Create netParams of the full model based on the config
    netParams_full = create_net_params(cfg)
    
    # Load firing rates and spike times data from a previous simulation for subnet builder
    dirpath_old_sim = Path(r'/ddn/niknovikov19/repo/A1_model_old/data/A1_paper')
    tlim = (1, 4)
    old_sim_name = 'v34_batch56_10s'
    postfix = f'(t={tlim[0]}-{tlim[1]})'
    fpath_rates = dirpath_old_sim / f'{old_sim_name}_pop_rates_{postfix}.pkl'
    fpath_spikes = dirpath_old_sim / f'{old_sim_name}_spikes_{postfix}.pkl'
    sim_data = {}
    with open(fpath_rates, 'rb') as fid:
        sim_data['rates'] = pkl.load(fid)
    with open(fpath_spikes, 'rb') as fid:
        sim_data['spikes'] = pkl.load(fid)
    sim_data['spikes'] = {pop: [list(s) for s in spikes] for pop, spikes in sim_data['spikes'].items()}
        
    #return sim_data
    
    # Create subnet netParams
    desc = subnet_mod.prepare_subnet_desc(sim_data, cfg)
    spb = SubnetParamBuilder()    
    netParams_sub = spb.build(netParams_full.todict(), desc)
    netParams_sub = specs.NetParams(netParams_sub)
    
    comm.initialize()
    
    # Save the config into the output folder
    if comm.is_host(): #or not is_batch:
        cfg.save(str(dirpath_exp / f'{exp_name}_cfg.json'))
        netParams_full.save(str(dirpath_exp / f'{exp_name}_netParams_full.json'))
        netParams_sub.save(str(dirpath_exp / f'{exp_name}_netParams_sub.json'))
        
    cfg.singleCellPops = 1
    
    # Prepare simulation
    sim.initialize(simConfig=cfg, netParams=netParams_sub)
    sim.net.createPops()               			# instantiate network populations
    sim.net.createCells()              			# instantiate network cells based on defined populations
    #sim.net.connectCells()            			# create connections between cells based on params
    sim.net.addStims() 							        # add network stimulation
    
    return
    
    # Run simulations
    sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
    sim.runSim()                      			# run parallel Neuron simulation  
    sim.gatherData()                  			# gather spiking data and cell info from each node
    
    # Save the results
    sim.saveData()
    sim.analysis.plotData()         			# plot spike raster etc
    
    # Close the communication with the batchtools master process
    if is_batch and comm.is_host():
       out_json = json.dumps({'loss': 0})
       comm.send(out_json)
       comm.close()
