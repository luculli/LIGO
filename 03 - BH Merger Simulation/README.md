# Dockerfile for BH Merger SImulation - v0.1
A simple simulator of the merging of BH is implemented in Python. The main idea is that the initial spatial distribution
of BH and a limited range effect of their interaction could be sufficient to establish the main characteristics of the BHDF
(i.e. gaps existence, etc). The merging would essentially be a topological effect in that case.

Main adopted hypothesis:

* the space of simulation is a 2-dimensional grid of NxN
* the initial spatial distribution of BH is uniform in the whole grid but it is limited to a small percentage of the grid size
* each BH has a mass which is picked by a uniform distribution between 1 and a maximum value
* merging rule 1: two BH can meger only if their distance is less that a given parameter which is a constant for the whole simulation
* merging rule 2: when two BHs merge the new BH is located in the baricenter of the two
