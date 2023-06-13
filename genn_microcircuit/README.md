# Cortical microcircuit model for GeNN

Taken from https://github.com/BrainsOnBoard/pygenn_paper/tree/master/models/potjans_microcircuit
The file [potjans_microcircuit_pygenn.py](potjans_microcircuit_pygenn.py) is under the MIT licence:
```
MIT License

Copyright (c) 2023 Brains on Board

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
<br>
Time of writing: 11.03.2023, last update to model: 25.01.2021

## Prerequisites

These scripts were tested with GeNN simulator version 4.8.0
Installation instructions can be found at:
 - https://genn-team.github.io/genn/documentation/4/html/d8/d99/Installation.html

<br>

Additionally to run the scripts to post process the data, Python and additional packages are required.
To run the data post processing scripts we used:
 * Python 3.8.6
 * Numpy 1.22

## Contents

### Modified files

These files were modified for benchmarking purposes:
 - [potjans_microcircuit_pygenn.py](potjans_microcircuit_pygenn.py):
   - Changed default value of BUILD_MODEL parameter [L38](potjans_microcircuit_pygenn.py#L38). By default its value is False which causes the simulation to fail if the model was not previously built. Changed to True.

### Additional files

These files were added for benchmarking purposes:
 - [run_benchmark.py](run_benchmark.py): Python script based on the original simulation script of the model with additional adaptations for benchmarking, notably the addition of command line argument handling, simulation timers (cf Models sub-section in #INSERT PAPER REF#), and data exporting to json files.
   - Modified initial conditions of membrane potential ([L218](run_benchmark.py#L218) and [L242](run_benchmark.py#L242)) to use "optimized" parameters such as those used by NEST GPU and NEST cortical microcircuit.
 - [gather_data.py](gather_data.py): Python script designed to collect the data from all of the simulation runs of a benchmark and compute the mean values and the standard deviation of the simulation timers.
 - [benchmark.sh](benchmark.sh): Bash script to automatically benchmark the model with 10 different random generation seeds and collect the data.
 
## Execution

To run a 10 simulation benchmark using 10 different random generation seeds:
```shell
bash benchmark.sh
```

By default this script runs on local machines, this can be changed to run with SLURM in an interactive session by commenting [L41](benchmark.sh#L41) and uncommenting [L44](benchmark.sh#L44).
