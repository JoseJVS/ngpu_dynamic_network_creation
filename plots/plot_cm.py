import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cifre=17
titolo=18

# NEST simulations
nest_1node_build = 20
nest_1node_build_std = 1.0
nest_1node_simulation = 14.0/10.0
nest_1node_simulation_std = 1.5/10.0

nest_2node_build = 18
nest_2node_build_std = 1.5
nest_2node_simulation = 12.0/10.0
nest_2node_simulation_std = 1.5/10.0

nest_3node_build = 15
nest_3node_build_std = 1.5
nest_3node_simulation = 10.0/10.0
nest_3node_simulation_std = 1.5/10.0

# JURECA simulations
ngpu_main_A100_build = 20
ngpu_main_A100_build_std = 0.5
ngpu_main_A100_simulation = 11.0/10.0
ngpu_main_A100_simulation_std = 1.5/10.0

ngpu_conn_A100_build = 0.5
ngpu_conn_A100_build_std = 0.01
ngpu_conn_A100_simulation = 11.0/10.0
ngpu_conn_A100_simulation_std = 1.6/10.0

genn_A100_build = 25
genn_A100_build_std = 1.0
genn_A100_simulation = 13.0/10.0
genn_A100_simulation_std = 1.6/10.0

# JUSUF simulations
ngpu_main_V100_build = 18
ngpu_main_V100_build_std = 0.5
ngpu_main_V100_simulation = 10.5/10.0
ngpu_main_V100_simulation_std = 1.5/10.0

ngpu_conn_V100_build = 0.4
ngpu_conn_V100_build_std = 0.01
ngpu_conn_V100_simulation = 10.5/10.0
ngpu_conn_V100_simulation_std = 1.6/10.0

genn_V100_build = 26
genn_V100_build_std = 1.0
genn_V100_simulation = 14.0/10.0
genn_V100_simulation_std = 1.6/10.0

#pcgolosio3 simulations
ngpu_main_2080_build = 17
ngpu_main_2080_build_std = 0.5
ngpu_main_2080_simulation = 10.0/10.0
ngpu_main_2080_simulation_std = 1.5/10.0

ngpu_conn_2080_build = 0.35
ngpu_conn_2080_build_std = 0.01
ngpu_conn_2080_simulation = 10.0/10.0
ngpu_conn_2080_simulation_std = 1.6/10.0

genn_2080_build = 23
genn_2080_build_std = 1.0
genn_2080_simulation = 12.0/10.0
genn_2080_simulation_std = 1.6/10.0


simulators=['NEST GPU main', 'NEST GPU conn', 'GeNN']
gpu_colors = ['orange', 'cornflowerblue', 'forestgreen']
A100 = [ngpu_main_A100_build, ngpu_conn_A100_build, genn_A100_build]
A100std = [ngpu_main_A100_build_std, ngpu_conn_A100_build_std, genn_A100_build_std]
V100 = [ngpu_main_V100_build, ngpu_conn_V100_build, genn_V100_build]
V100std = [ngpu_main_V100_build_std, ngpu_conn_V100_build_std, genn_V100_build_std]
RTX2080Ti = [ngpu_main_2080_build, ngpu_conn_2080_build, genn_2080_build]
RTX2080Tistd = [ngpu_main_2080_build_std, ngpu_conn_2080_build_std, genn_2080_build_std]
CPU = [nest_1node_build, nest_2node_build, nest_3node_build]
CPUstd = [nest_1node_build_std, nest_2node_build_std, nest_3node_build_std]

x_axis = np.arange(len(simulators))

# build time plot with different hardware and simulators
plt.figure(1, figsize=(16, 9), dpi=300)
nest_loc = [-0.2, 0.0, 0.2]
nest_colors = ['coral', 'orangered', 'darkred']
for i in range(len(CPU)):
    plt.bar(x=nest_loc[i], height=CPU[i], width=0.2, color=nest_colors[i], label = 'CPU ' + str(i+1) + ' node', zorder=3)
    plt.bar(x=nest_loc[i], height=CPU[i], width=0.2, color='none', yerr=CPUstd[i], capsize=5, error_kw={"elinewidth": 2.25}, zorder=3)

plt.bar(x=1+x_axis - 0.2, height=RTX2080Ti, width=0.2, color = gpu_colors[0], label = 'NVIDIA RTX 2080Ti', zorder=3)
plt.bar(x=1+x_axis - 0.2, height=RTX2080Ti, width=0.2, color = 'none', yerr=RTX2080Tistd, capsize=5, error_kw={"elinewidth": 2.25}, zorder=3)
plt.bar(x=1+x_axis, height=V100, width=0.2, color = gpu_colors[1], label = 'NVIDIA V100', zorder=3)
plt.bar(x=1+x_axis, height=V100, width=0.2, color = 'none', yerr=V100std, capsize=5, error_kw={"elinewidth": 2.25}, zorder=3)
plt.bar(x=1+x_axis + 0.2, height=A100, width=0.2, color = gpu_colors[2], label = 'NVIDIA A100', zorder=3)
plt.bar(x=1+x_axis + 0.2, height=A100, width=0.2, color = 'none', yerr=A100std, capsize=5, error_kw={"elinewidth": 2.25}, zorder=3)
plt.yscale('log')
plt.ylim(0,100)
plt.xticks(np.arange(len(simulators) + 1), ["NEST 3.3"] + simulators, fontsize=cifre+4)
plt.ylabel('Build time [s]', fontsize=cifre+4)
plt.tick_params(labelsize=cifre+2)
plt.legend(title="Simulation hardware", ncol=2, fontsize=cifre-4, title_fontsize=cifre-4, framealpha=1.0)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.draw()
plt.savefig("build_time_cm.png")

#plt.show()
# overall simulation time (i.e. build + simulation) for a given hardware using different simulators
plt.figure(2, figsize=(16, 9), dpi=300)
import tol_colors
light = tol_colors.tol_cset('light')
# same colors used from beNNch 
total_time_colors = [light.light_cyan, light.pink]
# hardware: NVIDIA A100, 1 CPU
xax = ['NEST', 'NEST GPU main', 'NEST GPU conn', 'GeNN']
ybt = [nest_1node_build, ngpu_main_A100_build, ngpu_conn_A100_build, genn_A100_build]
yerrbt = [nest_1node_build_std, ngpu_main_A100_build_std, ngpu_conn_A100_build_std, genn_A100_build_std]
yst = [nest_1node_simulation, ngpu_main_A100_simulation, ngpu_conn_A100_simulation, genn_A100_simulation]
yerrst = [nest_1node_simulation_std, ngpu_main_A100_simulation_std, ngpu_conn_A100_simulation_std, genn_A100_simulation_std]

plt.bar(x=xax, height=ybt, width=0.6, color=total_time_colors[0], label = "Network construction", zorder=3)
plt.bar(x=xax, height=yst, width=0.6, color=total_time_colors[1], bottom=ybt, label = "State propagation", zorder=3)
plt.bar(x=xax, height=ybt, color='none', yerr=yerrbt, capsize=5, error_kw={"elinewidth": 2.25}, zorder=3)
plt.bar(x=xax, height=yst, color='none', yerr=yerrst, bottom=ybt, capsize=5, error_kw={"elinewidth": 1.25}, zorder=3)
plt.ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$' + f'10 s',fontsize=cifre+4)
plt.yscale('log')
plt.ylim(0,100)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.xticks(fontsize=cifre+4)
plt.yticks(fontsize=cifre)
plt.legend(fontsize=cifre-4, framealpha=1.0)
plt.draw()
plt.savefig("total_time_cm.png")
plt.show()
