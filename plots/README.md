# Plotting scripts

Plotting scripts used to generate figures for #INSERT PAPER REF#

## Contents

### Cortical Microcircuit

[plot_cm.py](plot_cm.py) to generate figures #INSERT FIGURE REF# from #INSERT PAPER REF#, [cm_net_constr.pdf](cm_net_constr.pdf), and [cm_tot.pdf](cm_tot.pdf) respectively.
<br>
To generate new plots from new data, the scripts assumes that the data to be loaded follows the structure given by the ```gather_data.py``` script in the model directories.
Furthermore it is necessary to update the paths in lines [L24](plot_cm.py#L24) - [L36](plot_cm.py#L36) with the desired directories containing the corresponding new data.
<br>
To execute:
```shell
python3 plot_cm.py
```
