"""
init.py

Starting script to run NetPyNE-based A1 model.


Usage:
    python init.py # Run simulation, optionally plot a raster


MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py


Contributors: ericaygriffith@gmail.com, salvadordura@gmail.com
"""

from IPython import embed
import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from mpi4py import MPI

from netpyne import sim

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')

# sim.createSimulateAnalyze(netParams, cfg)

sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  				# create network object and set cfg and net params
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations

sim.pc.barrier()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
pop_name = 'PV5B'
gids = sim.net.pops[pop_name].cellGids
print(f'==== {len(gids)} cells of type {pop_name} on the core {rank} ====')
sim.pc.barrier()

#sim.net.connectCells()            			# create connections between cells based on params
#sim.net.addStims() 							# add network stimulation

#sim.pc.barrier()
#if sim.rank == 0:
#    embed()
#sim.pc.barrier()

#sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
#sim.runSim()                      			# run parallel Neuron simulation  
#sim.gatherData()                  			# gather spiking data and cell info from each node

# distributed saving (to avoid errors with large output data)
#sim.saveDataInNodes()
#sim.gatherDataFromFiles()

#sim.saveData()  

#sim.analysis.plotData()         			# plot spike raster etc
