import importlib.util
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

from netpyne.batchtools import comm
from netpyne import sim

from create_base_cfg_v34_batch56 import create_base_cfg
from create_net_params import create_net_params


#exp_name = 'test_run_1'
#is_batch = False


def run_exp(exp_name, is_batch):
    
    # Import experiment-specific config py-file
    fpath_exp_cfg = Path(__file__).resolve().parent / exp_name / 'exp_cfg.py'
    cfg_mod_spec = importlib.util.spec_from_file_location(
        'module.name', fpath_exp_cfg)
    cfg_mod = importlib.util.module_from_spec(cfg_mod_spec)
    sys.modules['module.name'] = cfg_mod
    cfg_mod_spec.loader.exec_module(cfg_mod)
    
    # Initialize config object, common for every experiment of the model
    cfg = create_base_cfg()
    
    # Apply experiment-specific config modifications
    cfg_mod.apply_exp_cfg(cfg)
    
    # Automatically set the experiment name in config
    cfg.simLabel = exp_name
    cfg.saveFolder = str(Path(__file__).resolve().parent.parent.parent / 'data' / exp_name)
    
    # Update config by batchtools
    cfg.update_cfg()
    
    # Create netParams based on the config
    netParams = create_net_params(cfg)
    
    comm.initialize()
    
    # Save the config into the output folder
    if comm.is_host(): #or not is_batch:
        cfg.save("{}/{}_params.json".format(cfg.saveFolder, cfg.simLabel))
    
    # Prepare simulation
    sim.initialize(simConfig=cfg, netParams=netParams)
    sim.net.createPops()               			# instantiate network populations
    sim.net.createCells()              			# instantiate network cells based on defined populations
    sim.net.connectCells()            			# create connections between cells based on params
    sim.net.addStims() 							        # add network stimulation
    
    # Run simulation
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
