
def apply_exp_cfg(cfg):
    
    cfg.duration = 3 * 1e3
    
    cfg.analysis['plotRaster'] = {
        'include': cfg.allpops, 'saveFig': True, 'showFig': False,
        'popRates': True, 'orderInverse': True, 'timeRange': [100, cfg.duration],
        'figSize': (14, 12), 'lw': 0.3, 'markerSize': 3, 'marker': '.', 'dpi': 300
    }
    cfg.analysis['plotSpikeStats'] = {
        'stats': ['rate', 'isicv'], 'figSize': (6, 12),
        'timeRange': [100, cfg.duration], 'dpi': 300, 'showFig': 0, 'saveFig': 1
    }
    
    cfg.subnet_par = {
        'pops_active': ['IT3', 'SOM3', 'PV3', 'VIP3', 'NGF3'],
        #'inp_type': 'poisson'
        'inp_type': 'spike_replay'
    }
