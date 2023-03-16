# Plotting scripts

Plotting scripts used to generate figures for #INSERT PAPER REF#

## Prerequisites

Additionally to generate plots, Python and additional packages are required.
To run the data post processing scripts and plotting scripts the following software was used:
 * Python 3.8.6
 * Matplotlib 3.5
 * Tol Colors 1.2.1 (https://pypi.org/project/tol-colors/)

## Contents

### Cortical Microcircuit

[plot_cm.py](plot_cm.py) to generate figures #INSERT FIGURE REF# from #INSERT PAPER REF#, [cm_net_constr.pdf](cm_net_constr.pdf), and [cm_tot.pdf](cm_tot.pdf) respectively.

<br>

To generate new plots from new data, the scripts assumes that the data to be loaded follows the structure given by the ```gather_data.py``` script in the model directories.
Furthermore it is necessary to update the paths in lines [L24](plot_cm.py#L24) - [L36](plot_cm.py#L36) with the desired directories containing the corresponding new data.

## Execution

To generate the microcircuit plots:
```shell
python3 plot_cm.py
```
