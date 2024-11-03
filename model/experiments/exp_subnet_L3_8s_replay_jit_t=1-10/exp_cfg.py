import os

def apply_exp_cfg(cfg):
    
    cfg.duration = 8 * 1e3
    
    cfg.analysis['plotRaster'] = {
        'include': cfg.allpops, 'saveFig': True, 'showFig': False,
        'popRates': True, 'orderInverse': True, 'timeRange': [100, cfg.duration],
        'figSize': (14, 12), 'lw': 0.3, 'markerSize': 3, 'marker': '.', 'dpi': 300
    }
    cfg.analysis['plotSpikeStats'] = {
        'stats': ['rate', 'isicv'], 'figSize': (6, 12),
        'timeRange': [100, cfg.duration], 'dpi': 300, 'showFig': 0, 'saveFig': 1
    }
    
    # Spikes/rates used for input generation by frozen pops.
    dirpath_old_sim = '/ddn/niknovikov19/repo/A1_model_old/data/A1_paper'
    tlim = (1, 10)
    old_sim_name = 'v34_batch56_10s'
    postfix = f'(t={tlim[0]}-{tlim[1]})'
    fpath_rates = os.path.join(dirpath_old_sim, f'{old_sim_name}_pop_rates_{postfix}.pkl')
    fpath_spikes = os.path.join(dirpath_old_sim, f'{old_sim_name}_spikes_{postfix}.pkl')
    
    cfg.subnet_par = {
        'pops_active': ['IT3', 'SOM3', 'PV3', 'VIP3', 'NGF3'],
        #'inp_type': 'poisson'
        'inp_type': 'spike_replay_jit',
        'fpath_inp_rates': fpath_rates,
        'fpath_inp_spikes': fpath_spikes
    }
