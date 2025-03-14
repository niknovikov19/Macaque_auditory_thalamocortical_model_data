
def get_batch_params():
    
    params = {
        'subnet_par.pops_active': [
            ['IT2', 'SOM2', 'PV2', 'VIP2', 'NGF2'],
            ['IT3', 'SOM3', 'PV3', 'VIP3', 'NGF3'],
            ['ITP4', 'ITS4', 'SOM4', 'PV4', 'VIP4', 'NGF4'],
            ['IT5A', 'CT5A', 'SOM5A', 'PV5A', 'VIP5A', 'NGF5A'],
            ['IT5B', 'CT5B', 'PT5B', 'SOM5B', 'PV5B', 'VIP5B', 'NGF5B'],
            ['IT6', 'CT6', 'SOM6', 'PV6', 'VIP6', 'NGF6']
        ],
        'subnet_par.inp_type': [
            'poisson',
            'spike_replay',
            'spike_replay_jit'
        ]
    }
    
    return params

