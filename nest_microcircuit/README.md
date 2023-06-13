# Cortical microcircuit model for NEST

Taken from https://github.com/nest/nest-simulator/tree/master/pynest/examples/Potjans_2014
<br>
Time of writing: 11.03.2023, last update to model: 01.02.2023

<br>

To reproduce the performance shown in the data for the NEST simulations it is needed to use high-performance computing systems, the systems used for the paper are described in the "Hardware and Software" subsection in #INSERT PAPER REF#

## Prerequisites

These scripts were tested with NEST simulator version 3.3
Installation instructions can be found at:
 - https://nest-simulator.readthedocs.io/en/v3.3/installation/index.html

<br>

Furthermore to run the full scaled microcircuit in a compute node, while taking all the advantage of compute power, MPI usage is required.

<br>

To obtain the same network construction times as in the #INSERT PAPER REF#, [jemalloc](https://github.com/jemalloc/jemalloc) is needed.
To allow NEST to take advantage of its functionalities, exporting the path to the compiled, shared library is needed:
```shell
export LD_PRELOAD=PATH_TO/libjemalloc.so
```
\[Optional]: This can be set in [L23](benchmark.sh#L23) of [benchmark.sh](benchmark.sh) script.

<br>

Additionally to run the scripts to post process the data, Python and additional packages are required.
To run the data post processing scripts we used:
 * Python 3.8.6
 * Numpy 1.22

## Contents

### Original files

These files did not change with respect to the source at time of writing:
 - [run_microcircuit.py](run_microcircuit.py)
 - [helpers.py](helpers.py)
 - [sim_params.py](sim_params.py)
 - [network_params.py](network_params.py)
 - [stimulus_params.py](stimulus_params.py)


### Modified files

These files were modified for benchmarking purposes:
 - [network.py](network.py):
    - Disabled Prepare and Cleanup call from connect function [L98](network.py#L98): To properly measure calibration time, Prepare and Cleanup functions were commented: [L126](network.py#L126) and [L127](network.py#L127).
    - Fixed MPI related bug at __setup_nest function [L263](network.py#L263) see pull request [2749](https://github.com/nest/nest-simulator/pull/2749) in NEST github repository.

### Additional files

These files were added for benchmarking purposes:
 - [run_benchmark.py](run_benchmark.py): Python script based on the original simulation script of the model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
    - Added handling of number of threads and processes passed as arguments.
    - Added computing of mean firing rate of neurons using the local_spike_counter kernel attribute.
 - [merge_data.py](merge_data.py): Python script to merge output of multiple MPI processes during a single simulation.
    - This Python script is meant to be run by the ```benchmark.sh``` script found in each model directory.
       - To run it individually, examples of local execution are found in each corresponding ```benchmark.sh```.
 - [gather_data.py](gather_data.py): Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - [benchmark.sh](benchmark.sh): Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
    - This script assumes the system used is equipped with 128 cores. By default the script allocates 8 MPI processes and 16 threads per process for the simulation. This can be changed in [L4](benchmark.sh#L4)-[L10](benchmark.sh#L10).
    - Additionally this script exploits OpenMP pinning and MPI binding to maximize simulation performance.
       - OpenMP pinning: [L25](benchmark.sh#L25)-[L28](benchmark.sh#L28)
       - MPI binding: [L48](benchmark.sh#L48), handled by SLURM
 
## Execution

To run a 10 simulation benchmark using 10 different random generation seeds:
```shell
bash benchmark.sh
```

By default this script runs with SLURM in an interactive session, this can be changed to run locally by commenting [L62](benchmark.sh#L62) and uncommenting [L59](benchmark.sh#L59).
Additionally setting the specific MPI executor (e.g. mpirun, mpiexec), the number of processes argument (e.g. -n, -np) and the MPI process binding is necessary.
