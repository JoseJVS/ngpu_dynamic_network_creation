# -*- coding: utf-8 -*-
#
# plot_tpn.py

"""

Plotting instructions for two-population network data.
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
import tol_colors

tick_fs = 15
legend_fs = 16
ylabel_fs = 18

# Define paths to data directories
data_path = "../simple_net/nestgpu_scaling/data_onboard/"

# dicts to store data
data = {"fixed_indegree": {"neurons": [], "conn_per_neuron": [], "constr_time": [], "constr_time_std": []},
        "fixed_outdegree": {"neurons": [], "conn_per_neuron": [], "constr_time": [], "constr_time_std": []},
        "fixed_total_number": {"neurons": [], "conn_per_neuron": [], "constr_time": [], "constr_time_std": []}}

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
                time_std = math.nan
            else:
                time = json_file['BlockStep']['timers']['time_construct']['mean']
                time_std = json_file['BlockStep']['timers']['time_construct']['std']
            #print("N {}, M {}, time {}".format(n, m, time))
            data[rule]["neurons"].append(n)
            data[rule]["conn_per_neuron"].append(m)
            data[rule]["constr_time"].append(time)
            data[rule]["constr_time_std"].append(time_std)
            jf.close()

# create DataFrames
df_fixed_indegree = pd.DataFrame(data["fixed_indegree"])
df_fixed_outdegree = pd.DataFrame(data["fixed_outdegree"])
df_fixed_total_number = pd.DataFrame(data["fixed_total_number"])


fig = plt.figure(1, figsize = (9,5), tight_layout = True)
colors = ["red", "blue", "green"]
linestyles = ["--", "-.", ":"]
for i, m in enumerate(connections):
    df = df_fixed_total_number[(df_fixed_total_number["conn_per_neuron"]==m)]
    #print(df)
    plt.errorbar(df["neurons"], df["constr_time"], yerr=df["constr_time_std"], marker="o", markersize=3, linestyle= linestyles[i], elinewidth=2.0, capsize=3.0, color = colors[i], label="K = {}".format(m))

plt.xlabel("Number of neurons (N)", fontsize=tick_fs)
plt.ylabel("Network construction time [s]", fontsize=tick_fs)
plt.tick_params(labelsize=tick_fs)
plt.xscale("log")
plt.yscale("log")
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.legend(title="Connections per neuron\n    fixed_total_number", fontsize=legend_fs-3, title_fontsize=legend_fs-3)

plt.savefig("fixed_total_number.pdf")

fig = plt.figure(2, figsize = (9,5), tight_layout = True)
for i, m in enumerate(connections):
    df = df_fixed_indegree[(df_fixed_indegree["conn_per_neuron"]==m)]
    #print(df)
    plt.errorbar(df["neurons"], df["constr_time"], yerr=df["constr_time_std"], marker="o", markersize=3, linestyle= linestyles[i], elinewidth=2.0, capsize=3.0, color = colors[i], label="K = {}".format(m))

plt.xlabel("Number of neurons (N)", fontsize=tick_fs)
plt.ylabel("Network construction time [s]", fontsize=tick_fs)
plt.tick_params(labelsize=tick_fs)
plt.xscale("log")
plt.yscale("log")
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.legend(title="Connections per neuron\n      fixed_indegree", fontsize=legend_fs-3, title_fontsize=legend_fs-3)

plt.savefig("fixed_indegree.pdf")

fig = plt.figure(3, figsize = (9,5), tight_layout = True)
for i, m in enumerate(connections):
    df = df_fixed_outdegree[(df_fixed_outdegree["conn_per_neuron"]==m)]
    #print(df)
    plt.errorbar(df["neurons"], df["constr_time"], yerr=df["constr_time_std"], marker="o", markersize=3, linestyle= linestyles[i], elinewidth=2.0, capsize=3.0, color = colors[i], label="K = {}".format(m))

plt.xlabel("Number of neurons (N)", fontsize=tick_fs)
plt.ylabel("Network construction time [s]", fontsize=tick_fs)
plt.tick_params(labelsize=tick_fs)
plt.xscale("log")
plt.yscale("log")
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.legend(title="Connections per neuron\n     fixed_outdegree", fontsize=legend_fs-3, title_fontsize=legend_fs-3)

plt.savefig("fixed_outdegree.pdf")

fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, figsize = (9,10), tight_layout = True)
ax1.text(-0.1, 1.05, "A", weight="bold", fontsize=ylabel_fs, color='k', transform=ax1.transAxes)
ax2.text(-0.1, 1.05, "B", weight="bold", fontsize=ylabel_fs, color='k', transform=ax2.transAxes)

for i, m in enumerate(connections):
    df_out = df_fixed_outdegree[(df_fixed_outdegree["conn_per_neuron"]==m)]
    ax2.errorbar(df_out["neurons"], df_out["constr_time"], yerr=df_out["constr_time_std"], marker="o", markersize=3, linestyle= linestyles[i], elinewidth=2.0, capsize=3.0, color = colors[i], label="K = {}".format(m))

    df_in = df_fixed_indegree[(df_fixed_indegree["conn_per_neuron"]==m)]
    ax1.errorbar(df_in["neurons"], df_in["constr_time"], yerr=df_in["constr_time_std"], marker="o", markersize=3, linestyle= linestyles[i], elinewidth=2.0, capsize=3.0, color = colors[i], label="K = {}".format(m))

ax1.set_xlabel("Number of neurons (N)", fontsize=tick_fs)
ax1.set_ylabel("Network construction time [s]", fontsize=tick_fs)
ax1.tick_params(labelsize=tick_fs)
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.grid(axis='y', which='major', alpha=0.75)
ax1.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
ax1.legend(title="Connections per neuron\n      fixed_indegree", fontsize=legend_fs-3, title_fontsize=legend_fs-3, framealpha=1.0)

ax2.set_xlabel("Number of neurons (N)", fontsize=tick_fs)
ax2.set_ylabel("Network construction time [s]", fontsize=tick_fs)
ax2.tick_params(labelsize=tick_fs)
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.grid(axis='y', which='major', alpha=0.75)
ax2.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
ax2.legend(title="Connections per neuron\n       fixed_outdegree", fontsize=legend_fs-3, title_fontsize=legend_fs-3, framealpha=1.0)

plt.savefig("fixed_indegree_outdegree.pdf")

#plt.show()
