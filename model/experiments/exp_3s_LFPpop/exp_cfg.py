
def apply_exp_cfg(cfg):
    
    cfg.duration = 3 * 1e3
    
    cfg.recordStep = 0.5
    cfg.recordLFP = [[100, y, 100] for y in range(0, 2000, 75)]
    cfg.saveLFPPops = ['IT2', 'IT3', 'ITP4', 'IT5A', 'IT5B', 'IT6', 'CT6']
    cell_idx = list(range(5))
    pops_rec = ['IT2', 'IT3', 'ITP4', 'IT5A', 'IT5B', 'IT6', 'CT6',
                'TC', 'HTC', 'IRE']
    cfg.recordCells = [(pop, cell_idx) for pop in pops_rec]
    cfg.recordTraces['V_soma'] = {"sec": "soma", "loc": 0.5, "var": "v"}
    cfg.recordTime = True
    
    cfg.analysis['plotRaster'] = {
        'include': cfg.allpops, 'saveFig': True, 'showFig': False,
        'popRates': True, 'orderInverse': True, 'timeRange': [100, cfg.duration],
        'figSize': (14, 12), 'lw': 0.3, 'markerSize': 3, 'marker': '.', 'dpi': 300
    }
    cfg.analysis['plotSpikeStats'] = {
        'stats': ['rate', 'isicv'], 'figSize': (6, 12),
        'timeRange': [100, cfg.duration], 'dpi': 300, 'showFig': 0, 'saveFig': 1
    }
