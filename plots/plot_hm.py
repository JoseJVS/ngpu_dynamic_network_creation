# -*- coding: utf-8 -*-
#
# plot_hm.py

"""

Plotting instructions for heatmaps data.
This script assumes that the data used was generated
by the benchmark.sh script in each model directory.

"""

import sys
import json
import numpy as np
import math
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import seaborn as sns
import tol_colors


tick_fs = 15
legend_fs = 16
ylabel_fs = 18

# Define paths to data directories
data_path = "../simple_net/nestgpu_scaling/data_onboard/"


# dicts to store data
data = {"fixed_indegree": {"neurons": [], "conn_per_neuron": [], "constr_time": []},
        "fixed_outdegree": {"neurons": [], "conn_per_neuron": [], "constr_time": []},
        "fixed_total_number": {"neurons": [], "conn_per_neuron": [], "constr_time": []}}

neurons = [1000, 10000, 100000, 1000000]
connections = [100, 1000, 10000]

# fill the data dict
for rule in ["fixed_indegree", "fixed_outdegree", "fixed_total_number"]:
    for n in neurons:
        for m in connections:
            jf = open(data_path + "benchmark_data_" + rule + "_" + str(m) + "_" + str(n) + "_2023-04-14_17-37-27.json")
            json_file = json.load(jf)
            if(json_file=={}):
                time = math.nan
            else:
                time = json_file['BlockStep']['timers']['time_construct']['mean']
            #print("N {}, M {}, time {}".format(n, m, time))
            data[rule]["neurons"].append(n)
            data[rule]["conn_per_neuron"].append(m)
            data[rule]["constr_time"].append(time)
            jf.close()

# create DataFrames for heatmap
df_fixed_indegree = pd.DataFrame(data["fixed_indegree"])
df_fixed_outdegree = pd.DataFrame(data["fixed_outdegree"])
df_fixed_total_number = pd.DataFrame(data["fixed_total_number"])

# plot heatmaps
gs = gridspec.GridSpec(2, 4)

fig = plt.figure(1, figsize = (10,7.5), tight_layout = True)

ax1 = plt.subplot(gs[0, :2])
ax2 = plt.subplot(gs[0, 2:])
ax3 = plt.subplot(gs[1, 1:3])

ax1.text(-0.1, 1.05, "A", weight="bold", fontsize=ylabel_fs, color='k', transform=ax1.transAxes)
ax1.set_title("fixed_indegree", fontsize=legend_fs)
sns.heatmap(df_fixed_indegree.pivot("conn_per_neuron", "neurons", "constr_time"), cmap="crest", norm=LogNorm(), square=True, annot=True, ax=ax1, cbar_kws={'shrink': 0.75})
ax1.set_xlabel("N", fontsize=tick_fs)
ax1.set_ylabel("M", fontsize=tick_fs)
ax2.set_title("fixed_outdegree", fontsize=legend_fs)
ax2.text(-0.1, 1.05, "B", weight="bold", fontsize=ylabel_fs, color='k', transform=ax2.transAxes)
sns.heatmap(df_fixed_outdegree.pivot("conn_per_neuron", "neurons", "constr_time"), cmap="crest", norm=LogNorm(), square=True, annot=True, ax=ax2, cbar_kws={'shrink': 0.75})
ax2.set_xlabel("N", fontsize=tick_fs)
ax2.set_ylabel("M", fontsize=tick_fs)
ax3.set_title("fixed_total_number", fontsize=legend_fs)
ax3.text(-0.1, 1.05, "C", weight="bold", fontsize=ylabel_fs, color='k', transform=ax3.transAxes)
sns.heatmap(df_fixed_total_number.pivot("conn_per_neuron", "neurons", "constr_time"), cmap="crest", norm=LogNorm(), square=True, annot=True, ax=ax3, cbar_kws={'shrink': 0.75})
ax3.set_xlabel("N", fontsize=tick_fs)
ax3.set_ylabel("M", fontsize=tick_fs)

plt.savefig("heatmap.pdf")

plt.show()

