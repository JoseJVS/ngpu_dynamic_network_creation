# Cortical microcircuit model for NEST GPU

Taken from https://github.com/nest/nest-gpu/tree/main/python/Potjans_2014
<br>
Time of writing: 11.03.2023, last update to model: 13.02.2023

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
   - Disabled Prepare and Cleanup call from connect function [L97](network.py#L97): To properly measure calibration time, Prepare and Cleanup functions were commented: [L125](network.py#L125) and [L126](network.py#L126).
   - Added get_network_size function to get total number of neurons: [L200](network.py#L200).

### Additional files

These files were added for benchmarking purposes:
 - [run_benchmark.py](run_benchmark.py): Python script based on the original simulation script of the model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
   - Added handling of different Nested Loop algorithms passed as argument.
 - [gather_data.py](gather_data.py): Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - [benchmark.sh](benchmark.sh): Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
   - By default, nested loop algorithm used is BlockStep, this can be changed in [L23](benchmark.sh#L23)
 - [run_recording.py](run_recording.py): Python script based on the original simulation script of the model with additional adaptations for multiple recording sessions, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
   - This Python script is meant to be run by the ```recording.sh``` script found in this directory.
     - To run it individually, examples of local execution and SLURM execution are found in ```recording.sh```.
   - In this script:
     - Spike recording is enabled.
     - Poisson generators are enabled.
     - Optimized membrane potentials are enabled.
     - Presimulation runs for 500ms.
     - Simulation runs for 10s.
- [recording.sh](recording.sh): Bash script to automatically run the model while recording spikes using 10 different random generation seeds and collect the data.
   - Can be used to run locally or through SLURM with an interactive session.
     - By default, it is set to run locally. To change this, uncomment respective line execution line in script. More information can be found in the READMEs of each model directory.
     - SLURM executions assume a system equipped with 128, this can be changed through ```cores``` variable at the beginning of each script.
 
## Execution

To run a 10 simulation benchmark using 10 different random generation seeds:
```shell
bash benchmark.sh
```

By default this script runs on local machines, this can be changed to run with SLURM in an interactive session by commenting [L58](benchmark.sh#L58) and uncommenting [L61](benchmark.sh#L61).

To run 10 simulations with recordings using 10 different random generation seeds:
```shell
bash recording.sh
```

By default this script runs on local machines, this can be changed to run with SLURM in an interactive session by commenting [L58](recording.sh#L58) and uncommenting [L61](recording.sh#L61).
