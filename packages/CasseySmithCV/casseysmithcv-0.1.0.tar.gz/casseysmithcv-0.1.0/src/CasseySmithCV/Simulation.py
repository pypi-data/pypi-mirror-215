import pandas as pd
import numpy as np
from multiprocessing import Pool
from itertools import product
from tqdm import tqdm


def FindState(
	row, stateCum): return stateCum[stateCum >= row['location']].index[0]


def CalcShare(row, totalEmp): return row['plantSize']/totalEmp


def defaultStateList(): return [0.002224058, 0.002306375, 0.00251064, 0.003013682, 0.003096761, 0.00313106, 0.003317795, 0.003517487, 0.004493848, 0.004534243, 0.004627993, 0.00482387400000001, 0.00534902, 0.0057324, 0.006151601, 0.007303265, 0.00830096599999999, 0.00851590200000001, 0.008929007, 0.00928113699999999, 0.010106584, 0.011340563, 0.01192897, 0.012328356,
								0.012369514, 0.013686571, 0.013898458, 0.014230772, 0.014583663, 0.017106499, 0.018349624, 0.019218516, 0.020087407, 0.020215455, 0.02044411, 0.021098828, 0.021238308, 0.021482208, 0.024649089, 0.027751949, 0.029004981, 0.0295057380000001, 0.0296139679999999, 0.030014878, 0.039014006, 0.043138956, 0.043327977, 0.055110609, 0.065874196, 0.080751302, 0.107366831]


def SimulatePlants(n, sigma, stateCum):
	plants = pd.DataFrame({'plantSize': np.random.lognormal(
		10, sigma, n), 'location': np.random.uniform(size=n)})
	plants['state'] = plants.apply(FindState, axis=1, args=(stateCum,))
	totalEmp = plants['plantSize'].sum()
	plants['share'] = plants.apply(CalcShare, axis=1, args=(totalEmp,))
	plants['sqshare'] = plants['share']**2
	return (plants['sqshare'].sum(), plants.groupby('state')['share'].sum())


def SimulateIndustry(n, sigma, statePop, stateCum, x):
	HHI, industryStates = SimulatePlants(n, sigma, stateCum)
	G = sum([(value - industryStates.loc[ind]) **
			 2 if ind in industryStates.index else value**2 for ind, value in statePop.items()])
	gamma = (G-(1-x)*HHI)/((1-x)*(1-HHI))
	return {'HHI': HHI, 'Gamma': gamma, 'G': G}


def runSimulation(n, sigma, stateList=defaultStateList(), R=100000, criticalValues=[0.025, 0.05, 0.95, 0.975], HHIConfInterval=[0.025, 0.05, 0.95, 0.975]):
	"""
	Create Gamma, G and HHI distribution and extracts specified critical values. 
	
	Parameters:
	-----------
	n : int
		Number of plants in the industry
	sigma : float
		Standard deviation of the underlying normal distribution
	stateList : list
		List of state shares (population weights).  Can be specified as population numbers or shares.  If unspecified, it defaults to the 1987 US population weights.  
	R : int
		Number of times to run each industry simulation.
	criticalValues : list
		List of critical values to extract from the empirical distributions of Gamma and G.  Defaults to [0.025, 0.05, 0.95, 0.975].
	HHIConfInterval : list
		List of critical values to extract from the empirical distribution of HHI. Defaults to [0.025, 0.05, 0.95, 0.975].
	
	Returns: 
		Dictionary:
			Plants : int
			Sigma : float
			GammaCV : Dictionary
			GCV : Dictionary
			HHICV : Dictionary

	"""

	statePop = pd.Series(stateList)
	totalPop = statePop.sum()
	if totalPop == 1:
		stateCum = statePop.cumsum()
	else:
		statePop = statePop/totalPop
		stateCum = statePop.cumsum()
	spq = statePop**2
	x = spq.sum()
	args = ((n, sigma, statePop, stateCum, x) for i in range(R))
	with Pool() as p:
		r = p.starmap(SimulateIndustry, args)
	rs = pd.DataFrame(r)
	ci = [rs['HHI'].quantile(q=civ) for civ in HHIConfInterval]
	gammaCV = [rs['Gamma'].quantile(q=civ) for civ in criticalValues]
	gCV = [rs['G'].quantile(q=civ) for civ in criticalValues]
	return {'Plants': n, 'Sigma': sigma, 'GammaCV': dict(zip(criticalValues, gammaCV)), 'GCV': dict(zip(criticalValues, gCV)), 'HHICV': dict(zip(HHIConfInterval, ci))}

def SimulationTable(ns, sigmas, stateList=defaultStateList(), R=100000, criticalValues=[0.025, 0.05, 0.95, 0.975], HHIConfInterval=[0.025, 0.05, 0.95, 0.975]):
	"""
	Create Gamma, G and HHI distributions and extracts specified critical values. 
	
	Parameters:
	-----------
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
	
	Returns:
	--------
	Pandas Dataframe with:
		Plants
		Sigma
		GammaCV
		GCV
		HHICV
	"""
	loops = list(product(ns, sigmas))
	r = []
	for row in tqdm(loops):
		r.append(runSimulation(row[0], row[1], stateList, R, criticalValues, HHIConfInterval))
	return pd.DataFrame(r)

