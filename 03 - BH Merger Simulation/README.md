# Dockerfile for BH Merger Simulation - v0.3
A simple simulator of the merging of BH is implemented in Python. The main idea is that the initial spatial distribution
of BH and a limited range effect of their interaction could be sufficient to establish the characteristics of the final BHDF
(i.e. mass gaps, mass density funciton, etc). The merging would essentially be a topological effect in that case.

Main adopted hypothesis:

* the space of simulation is a 2-dimensional grid of NxN points
* the initial spatial distribution of BH is uniform in the whole grid but it is limited to a small percentage of the grid size
* each BH has a mass which is picked by a uniform distribution between 1 and a maximum value

* merging rule 1: two BH can merge only if their distance is less that a given parameter which is a constant for the whole simulation
* merging rule 2: when two BHs merge the new BH is located in the baricenter of the two original BHs
* merging rule 3: the new Bh has a mass which is the sum of the original masses less the radiated energy


Parameters of the simulator:

* --grid-size : this is the value of N (default value 100)
* --max-dist  : this is the maxiaml distance between two BH to have a merger (default value 5)
* --zero-mass-density : this is the percentage of the NxN grid which is not filled by any BHs (default value 0.90)
* --run-type : this parameter can have two possible values, 1 and 2. When it is 1, the simulator generate a single grid of BHs and it computes its evolution, the output is the a signle realization of the final mass distribution. Instead, when the type is equal to 2, a set of 1000 grids are generated in parallel and the output is the global statitic of mass distribution (default value 1)

 
Examples of runs:

* python bh-life-v2.py
* python bh-life-v2.py --max-dist 10 --grid-size 200
* python bh-life-v2.py --run-type 2 --max-dist 10

