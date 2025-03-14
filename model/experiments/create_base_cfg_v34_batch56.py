from netpyne.batchtools import specs
import json


def create_base_cfg():
    
    # Load config that corresponds to Fig. 4A
    fpath_cfg = 'v34_batch56_0_0_cfg.json'
    with open(fpath_cfg, 'r') as fid:
        cfg_dict = json.load(fid)
    cfg = specs.SimConfig(cfg_dict['simConfig'])
    
    # Default duration
    cfg.duration = 1 * 1e3
    
    # Default recording params
    print(cfg.__dict__.keys())
    cfg.analysis['plotRaster'] = {'include': cfg.allpops, 'saveFig': True, 'showFig': False, 'popRates': True, 'orderInverse': True, 'timeRange': [1000, cfg.duration], 'figSize': (14,12), 'lw': 0.3, 'markerSize': 3, 'marker': '.', 'dpi': 300}      	## Plot a raster
    cfg.analysis['plotSpikeStats'] = {'stats': ['rate', 'isicv'], 'figSize': (6,12), 'timeRange': [1000, cfg.duration], 'dpi': 300, 'showFig': 0, 'saveFig': 1}
    
    cfg.wmult_rec = 1
    cfg.wmult_ebkg = 1
    
    # Scaling factor for TC and HTC leak conduction (default: no scaling)
    cfg.TC_leak_mult = 1
    cfg.TC_ebkg_mult = 1
    cfg.IRE_ibkg_mult = 1
    
    # Oscillatory input
    cfg.osc_inp_on = 0    # default: oscillatory input is off
    cfg.osc_pop_name = 'IT3'
    cfg.osc_A_frac = 0.8
    cfg.osc_f = 20
    cfg.osc_inp_indep = 1
    cfg.osc_pop_scale = 0.5
    cfg.osc_inp_replace_bkg = 1
    cfg.osc_inp_weight = 0
    
    return cfg