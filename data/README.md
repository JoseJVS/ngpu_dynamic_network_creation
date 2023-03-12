# Data

This directory contains the data generated for #INSERT PAPER REF#.
<br>
To generate new data, check the model directories available in this repo, for more information: [README](../README.md).

## Contents

The available directories are named after the simulator used to generate the data and the platform where it was simulated, i.e.
 - [genn_20280](genn_20280): GeNN simulator using RTX 2080Ti from "Workstation 1" described in "Hardware and Software" subsection of #INSERT PAPER REF#.
 - [nest_jureca](nest_jureca): NEST simulator using 1 node of the JURECA-DC cluster described in "Hardware and Software" subsection of #INSERT PAPER REF#.
 - [nestgpu_jusuf](nestgpu_jusuf): NEST GPU simulator using 1 node equipped with a V100 GPU of the JUSUF cluster described in "Hardware and Software" subsection of #INSERT PAPER REF#.

<br>

Depending on the simulator, a single or multiple data sets can be found, the directory hierarchy will be described in the next sections.
<br>
For each benchmarked model, the data from each seed was kept along the standard output stream and standard error stream of the execution.
<br>
The "gathered" data is found at the top of each benchmark data directory and named as ```benchmark_data_SIMULATION_ID.json``` with the simulation ID being composed of the date and time of running the benchmark.

### Cortical Microcircuit Data

[GeNN](genn_2080) directory contains a single set of microcircuit benchmarking data.
<br>
NEST and NEST GPU directories contain data sets for microcircuit benchmarks using DC inputs or poisson generators.
<br>
NEST GPU directories contain benchmarking sets for both the "main" version and "conn" version described in [README](../README.md).

### Balanced random network with Izhikevich neurons

TODO