# Cortical microcircuit model for GeNN

Taken from https://github.com/BrainsOnBoard/pygenn_paper/tree/master/models/potjans_microcircuit
<br>
Time of writing: 11.03.2023, last update to model: 25.01.2021

## Contents

### Original files

<br>

### Modified files

These files were modified for benchmarking purposes:
 - potjans_microcircuit_pygenn.py:
   - Changed default value of BUILD_MODEL parameter (l38). By default its value is False which causes the simulation to fail if model was not previously buitl.

### Additional files

These files were added for benchmarking purposes:
 - run_benchmark.py: Python script based on the original simulation script of the model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
  - Modified initial conditions of membrane potential (l218 - l242) to use "optimized" parameters such as those used by NEST GPU and NEST cortical microcircuit.
 - gather_data.py: Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - benchmark.sh: Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
 