from mpi4py import MPI
from neuron import h
import numpy as np

def calc_num_cells(netParams, pop_name):
    from numpy import pi
    par = netParams.popParams[pop_name]
    if netParams.shape == 'cuboid':
        volume = netParams.sizeY / 1e3 * netParams.sizeX / 1e3 * netParams.sizeZ / 1e3
    elif netParams.shape == 'cylinder':
        volume = netParams.sizeY / 1e3 * netParams.sizeX / 1e3 / 2 * netParams.sizeZ / 1e3 / 2 * pi
    elif netParams.shape == 'ellipsoid':
        volume = netParams.sizeY / 1e3 / 2.0 * netParams.sizeX / 1e3 / 2.0 * netParams.sizeZ / 1e3 / 2.0 * pi * 4.0 / 3.0
    for coord in ['x', 'y', 'z']:
        if coord + 'normRange' in par:
            minv = par[coord + 'normRange'][0]
            maxv = par[coord + 'normRange'][1]
            volume = volume * (maxv - minv)
    return int(volume * par['density'])

def _generate_sin_spike_times(cfg, r0, A, f, ncells):
    '''Generate poisson spike trains with sinusoidally modulated rate. '''
    T = cfg.duration
    dt = cfg.dt
    tvec = np.arange(0, T, dt)
    rvec = r0 + A * np.sin (2 * np.pi * f * tvec / 1000)
    Nt = len(tvec)
    S = (np.random.rand(ncells, Nt) < (rvec * dt / 1000))
    S = [tvec[np.argwhere(S[n, :])].ravel().tolist()
                   for n in range(ncells)]
    return S

def generate_sin_spike_times(cfg, r0, A, f, ncells):
    pc = h.ParallelContext()
    pc.barrier()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0:
        S = _generate_sin_spike_times(cfg, r0, A, f, ncells)
    else:
        S = None
    S = comm.bcast(S, root=0)
    return S