# CasseySmithCV
 
Simulation software to generate critical values for the Ellison-Glaeser index (1997).  This is updated software from Cassey and Smith (2014); it modernizes the codebase and increases the performance of the simulations.

## Examples

Run a simulation of industries with 20 plants and sigma value of 1. 

```python
from CasseySmithCV import runSimulation, SimulationTable, SaveSimulationTable
resultDictionary = runSimulation(20,1)
```

Run all combinations of [20, 30] plants and [0.5, 1] sigma values:

```python
from CasseySmithCV import runSimulation, SimulationTable, SaveSimulationTable
resultDataFrame = SimulationTable([20, 30],[0.5, 1])
```

Run all combinations of [20, 30] plants and [0.5, 1] sigma values and save the results to a file:

```python
from CasseySmithCV import runSimulation, SimulationTable, SaveSimulationTable
SaveSimulationTable('filename.csv', [20, 30],[0.5, 1])
```

## Installation 

This package can be installed by using either the pip or conda command:

### Installing by pip

```
pip install CasseySmithCV
```

### Installing by conda

```
conda install -c tazzben casseysmithcv
```