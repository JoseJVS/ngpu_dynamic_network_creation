# Plotting scripts

Plotting scripts used to generate figures for #INSERT PAPER REF#.

## Contents

### Cortical Microcircuit

[plot_cm.py](plot_cm.py) to generate figures 3, 4, and A4 in the paper; [cm_net_constr.pdf](cm_net_constr.pdf), [cm_real_time_fact.pdf](cm_real_time_fact.pdf) and [cm_overall_real_time_fact.pdf](cm_overall_real_time_fact.pdf) respectively.

To generate new plots from new data, the scripts assumes that the data to be loaded follows the structure given by the ```gather_data.py``` script in the model directories.
Furthermore it is necessary to update the paths in lines [L24](plot_cm.py#L24) - [L50](plot_cm.py#L50) with the desired directories containing the corresponding new data.


### Two-populations network

[plot_tpn.py](plot_tpn.py) to generate figures 5 and A5 in the paper;[cm_net_constr.pdf](cm_net_constr.pdf), and [cm_tot.pdf](cm_tot.pdf) respectively.

To generate new plots from new data, the scripts assumes that the data to be loaded follows the structure given by the ```gather_data.py``` script in the model directories.
Furthermore it is necessary to update the paths in line [L30](plot_tpn.py#L30) with the desired directory containing the corresponding new data.


### COPASS algorithm

[copass_plot.py](copass_plot.py) to generate figure A1 in the paper, [copass.pdf](copass.pdf).

