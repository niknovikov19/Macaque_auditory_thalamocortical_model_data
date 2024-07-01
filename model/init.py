import json
import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers

from netpyne.batchtools import specs
from netpyne.batchtools import comm
from netpyne import sim
from netParams import netParams, cfg


comm.initialize()

if comm.is_host():
  cfg.save("{}/{}_params.json".format(cfg.saveFolder, cfg.simLabel))

sim.initialize(simConfig=cfg, netParams=netParams)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation

sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)
sim.runSim()                      			# run parallel Neuron simulation  
sim.gatherData()                  			# gather spiking data and cell info from each node

sim.saveData()  

sim.analysis.plotData()         			# plot spike raster etc

if comm.is_host():
  out_json = json.dumps({'loss': 0})
  comm.send(out_json)
  comm.close()
