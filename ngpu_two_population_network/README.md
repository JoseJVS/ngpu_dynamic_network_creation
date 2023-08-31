# Two population network model for NEST GPU

Created for network construction benchmarks, described in Models sub-section 2.4 and results shown in section 3 of:
<br>
<br>
Golosio, B.; Villamar, J.; Tiddia, G.; Pastorelli, E.; Stapmanns, J.; Fanti, V.; Paolucci, P.S.; Morrison, A.; Senk, J. Runtime Construction of Large-Scale Spiking Neuronal Network Models on GPU Devices. Appl. Sci. 2023, 13, 9598. https://doi.org/10.3390/app13179598
<br>

## Prerequisites

These scripts were tested with NEST GPU version tag [offboard](https://github.com/nest/nest-gpu/releases/tag/nest-gpu_offboard) and version tag [onboard](https://github.com/nest/nest-gpu/releases/tag/nest-gpu_onboard).
Installation instructions can be found at:
 - https://nest-gpu.readthedocs.io/en/latest/installation/index.html

<br>

Additionally to run the scripts to post process the data, Python and additional packages are required.
To run the data post processing scripts we used:
 * Python 3.8.6
 * Numpy 1.22

## Contents

The two population network is a simple model created for the sole purpose of network construction benchmarks.
It consists only of two neural populations connected to one another and connected to themselves.
There is no driving input to activate neural dynamics, in fact simulation is technically optional, however for completeness we set the time resolution to 1.0s and simulate for 1.0s.
Hence the neuron model was arbitrarily chosen to be the Izhikevich neuron model with all its parameters set to 0.
For the benchmarks we focused on the fixed indegree, fixed outdegree and fixed total number connectivity rules.

These files were added for benchmarking purposes:
 - [run_benchmark.py](run_benchmark.py): Python script for two population network model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in 2.4), and data exporting to json files.
   - Added handling of different Nested Loop algorithms passed as argument.
   - Added handling of neuron amount passed as argument.
   - Added handling of connection amount passed as argument.
   - Added handling of connectivity rule passed as argument.
 - [gather_data.py](gather_data.py): Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - [benchmark.sh](benchmark.sh): Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
   - By default, nested loop algorithm used is BlockStep, this can be changed in [L24](benchmark.sh#L24)
 
## Execution

To run a benchmark for the fixed indegree, outdegree and total number connectivity rules, using 1000, 10000, 100000, and 1000000 neurons, with 100, 1000, and 10000 connections each neuron, using 10 different random generation seeds:
```shell
bash benchmark.sh
```

By default this script runs on local machines, this can be changed to run with SLURM in an interactive session by commenting [L62](benchmark.sh#L62) and uncommenting [L65](benchmark.sh#L65).
