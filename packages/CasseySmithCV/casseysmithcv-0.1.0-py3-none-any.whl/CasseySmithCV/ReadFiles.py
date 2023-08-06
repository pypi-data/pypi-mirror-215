import os
from .Simulation import SimulationTable, defaultStateList

def importStateWeights(path):
    if os.path.exists(path):
        with open(path) as f:
            lst = f.read().splitlines()
            return [float(i) for i in lst]
    return []

def SaveSimulationTable(filename, ns, sigmas, stateList=defaultStateList(), R=100000, criticalValues=[0.025, 0.05, 0.95, 0.975], HHIConfInterval=[0.025, 0.05, 0.95, 0.975]):
    """
	Create Gamma, G and HHI distributions and extracts specified critical values. 
	
	Parameters:
	-----------
	filename : path
        Filename to save the results
    ns : list
		List of number of plants in the industry
	sigmas : list
		List of standard deviations of the underlying normal distribution
	stateList : list
		List of state shares (population weights).  Can be specified as population numbers or shares.  If unspecified, it defaults to the 1987 US population weights.  
	R : int
		Number of times to run each industry simulation.
	criticalValues : list
		List of critical values to extract from the empirical distributions of Gamma and G.  Defaults to [0.025, 0.05, 0.95, 0.975].
	HHIConfInterval : list
		List of critical values to extract from the empirical distribution of HHI. Defaults to [0.025, 0.05, 0.95, 0.975].
	
	"""
    d = SimulationTable(ns, sigmas, stateList, R, criticalValues, HHIConfInterval)
    d.to_csv(filename)
