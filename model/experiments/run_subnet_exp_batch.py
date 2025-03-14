import importlib.util
import json
import os
from pathlib import Path
import pickle as pkl
import sys

import matplotlib
matplotlib.use('Agg')  # to avoid graphics error on servers

from netpyne.batchtools import comm, specs
from netpyne import sim
from netpyne.specs import NetParams
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))

from subnet_tuner import SubnetDesc, SubnetParamBuilder
import subnet_tuner.sim_res_parse_utils as srp

from create_base_cfg_v34_batch56 import create_base_cfg
from create_net_params import create_net_params


def _load_module(fpath_mod):
    mod_spec = importlib.util.spec_from_file_location(
        'module.name', fpath_mod)
    mod = importlib.util.module_from_spec(mod_spec)
    sys.modules['module.name'] = mod
    mod_spec.loader.exec_module(mod)
    return mod


def _prepare_subnet_desc(sim_data: dict, cfg: specs.SimConfig) -> SubnetDesc:    
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
    elif cfg.subnet_par['inp_type'] == 'spike_replay_jit':
        for pop, spikes in sim_data['spikes'].items():
            if pop not in desc.pops_active:
                desc.inp_surrogates[pop] = {
                    'type': 'spike_replay_jit',
                    'spkTimes': spikes
                    }
                    
    return desc


def run_exp():
    
    # Preliminary: get cfg from batchtools to identify exp_name (simLabel),
    # which is then used to  generate the path to exp_cfg.py
    exp_name = specs.mappings['simLabel'][:-6]  # cut away job id
    
    # Import experiment-specific config py-file
    dirpath_exp = Path(__file__).resolve().parent / exp_name
    fpath_exp_cfg = dirpath_exp / 'exp_cfg.py'
    cfg_mod = _load_module(fpath_exp_cfg)
    
    # Initialize config object, common for every experiment of the model
    cfg = create_base_cfg()
    
    # Apply experiment-specific config modifications
    cfg_mod.apply_exp_cfg(cfg)
    
    # Update config by batchtools (including cfg.simLabel and cfg.saveFolder)
    cfg.update_cfg()
    
    # Create netParams of the full model based on the config
    netParams_full = create_net_params(cfg)
    
    # Load firing rates and spike times data from a previous simulation for subnet builder
    sim_data = {}
    with open(cfg['subnet_par']['fpath_inp_rates'], 'rb') as fid:
        sim_data['rates'] = pkl.load(fid)
    with open(cfg['subnet_par']['fpath_inp_spikes'], 'rb') as fid:
        sim_data['spikes'] = pkl.load(fid)
    sim_data['spikes'] = {pop: [list(s) for s in spikes] for pop, spikes in sim_data['spikes'].items()}
    
    # Create subnet netParams
    desc = _prepare_subnet_desc(sim_data, cfg)
    spb = SubnetParamBuilder()    
    netParams_sub = spb.build(netParams_full.todict(), desc)
    netParams_sub = NetParams(netParams_sub)
    
    comm.initialize()
    
    # Save cfg and netParams into the output folder
    if comm.is_host():
        os.makedirs(cfg.saveFolder, exist_ok=True)
        cfg.save('{}/{}_cfg.json'.format(cfg.saveFolder, cfg.simLabel))
        netParams_full.save(
            '{}/{}_netParams_full.json'.format(cfg.saveFolder, cfg.simLabel))
        netParams_sub.save(
            '{}/{}_netParams_sub.json'.format(cfg.saveFolder, cfg.simLabel))

    if True:
        # Prepare simulation
        sim.initialize(simConfig=cfg, netParams=netParams_sub)
        sim.net.createPops()               			# instantiate network populations
        sim.net.createCells()              			# instantiate network cells based on defined populations
        sim.net.connectCells()            			# create connections between cells based on params
        sim.net.addStims() 							# add network stimulation
        
        # Run simulations
        sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
        sim.runSim()                      			# run parallel Neuron simulation  
        sim.gatherData()                  			# gather spiking data and cell info from each node
        
        # Save the results
        sim.saveData()
        sim.analysis.plotData()         			# plot spike raster etc
  
    # Close the communication with the batchtools master process
    if comm.is_host():
        out_json = json.dumps({'loss': 0})
        comm.send(out_json)
        comm.close()
