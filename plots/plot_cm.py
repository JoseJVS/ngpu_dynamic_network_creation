import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys

tick_fs = 10
legend_fs = 11
ylabel_fs = 14


# NEST simulations [temporary]
nest_1node = json.load(open("../data/nest_jureca/fastest_1_node.json", "r"))
nest_1node = nest_1node['all']['timers']

nest_2node = json.load(open("../data/nest_jureca/fastest_2_node.json", "r"))
nest_2node = nest_2node['all']['timers']

# JURECA simulations
# load ngpu main
ngpu_main_A100 = json.load(open("../data/nestgpu_jureca/nestgpu_main_A100.json", "r"))
ngpu_main_A100 = ngpu_main_A100['BlockStep']

ngpu_conn_A100 = json.load(open("../data/nestgpu_jureca/nestgpu_conn_A100.json", "r"))
ngpu_conn_A100 = ngpu_conn_A100['BlockStep']

genn_A100 = json.load(open("../data/genn_jureca/genn_A100.json", "r"))

# JUSUF simulations
ngpu_main_V100 = json.load(open("../data/nestgpu_jusuf/nestgpu_main_V100.json", "r"))
ngpu_main_V100 = ngpu_main_V100['BlockStep']

ngpu_conn_V100 = json.load(open("../data/nestgpu_jusuf/nestgpu_conn_V100.json", "r"))
ngpu_conn_V100 = ngpu_conn_V100['BlockStep']

genn_V100 = json.load(open("../data/genn_jusuf/genn_V100.json", "r"))

#pcgolosio3 simulations
ngpu_main_2080 = json.load(open("../data/nestgpu_2080/nestgpu_main_2080.json", "r"))
ngpu_main_2080 = ngpu_main_2080['BlockStep']

ngpu_conn_2080 = json.load(open("../data/nestgpu_2080/nestgpu_conn_2080.json", "r"))
ngpu_conn_2080 = ngpu_conn_2080['BlockStep']

genn_2080 = json.load(open("../data/genn_2080/genn_2080.json", "r"))


simulators=['NEST', 'NEST GPU main', 'NEST GPU conn', 'GeNN']
# initialize, create, connect
ngpu_colors = ['orange', 'cornflowerblue', 'forestgreen', 'lightgreen']
# initialize, create, connect, code generation, load
genn_colors = ['yellow', 'steelblue', 'orangered']

nestgpu_keys = ["time_network", "time_create", "time_connect"]
genn_keys = ["time_network", "time_create", "time_connect", "time_build", "time_load"]

# build time plot with different hardware and simulators
plt.figure(1, figsize=(14, 9), dpi=300)
#plt.figure(1)
plt.subplot(2, 2, 1)
plt.text(-0.3,50.0,"A", weight="bold", fontsize=ylabel_fs)
nest_pos = [0.4, 0.75]
nest_data = [nest_1node, nest_2node]
for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_network"]["mean"], width=0.25, color = ngpu_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.25, bottom=nest_data[i]["time_network"]["mean"], color = ngpu_colors[1])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.25, bottom=nest_data[i]["time_network"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])

ngpu_main_pos = [1.2, 1.5, 1.8]
ngpu_main_data = [ngpu_main_V100, ngpu_main_A100, ngpu_main_2080]
for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_network"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_network"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_network"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_network"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[3])

ngpu_conn_pos = [2.2, 2.5, 2.8]
ngpu_conn_data = [ngpu_conn_V100, ngpu_conn_A100, ngpu_conn_2080]
for i in range(len(ngpu_conn_data)):
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_network"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])

genn_pos = [3.2, 3.5, 3.8]
genn_data = [genn_V100, genn_A100, genn_2080]
for i in range(len(genn_data)):
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])

plt.xticks(ticks=nest_pos + [0.575] + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node ", "2 nodes", "\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.ylim(1e-4,1e2)
plt.yscale('log')
#plt.ylim(0,75)
plt.ylabel('Network construction [s]', fontsize=ylabel_fs)
plt.tick_params(labelsize=tick_fs)
plt.tick_params(axis="x", length=0)
plt.grid(axis='y', which='major', alpha=0.75)
#plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)


################################################################
plt.subplot(2, 2, 2)
plt.text(-0.3,72.0,"B", weight="bold", fontsize=ylabel_fs)

for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_network"]["mean"], width=0.25, color = ngpu_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.25, bottom=nest_data[i]["time_network"]["mean"], color = ngpu_colors[1])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.25, bottom=nest_data[i]["time_network"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])

for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_network"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_network"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_network"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_network"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[3])

for i in range(len(ngpu_conn_data)):
    if i == 0:
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3], label = "Node calibration")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2], label = "Node connection")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"], color = ngpu_colors[1], label = "Node creation")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_network"]["mean"], width=0.2, color = ngpu_colors[0], label = "Initialization")
    else:
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_network"]["mean"], width=0.2, color = ngpu_colors[0])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"], color = ngpu_colors[1])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_network"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])

for i in range(len(genn_data)):
    if i==0:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2], label="Building")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1], label="Loading")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0], label="Model\ndefinition")
    else:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])

plt.xticks(ticks=nest_pos + [0.575] + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node ", "2 nodes", "\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.ylim(0,75)
plt.tick_params(labelsize=tick_fs)
plt.tick_params(axis="x", length=0)
plt.ylabel('Network construction [s]', fontsize=ylabel_fs)
plt.legend(title="Network construction phases", ncol=2, fontsize=legend_fs, title_fontsize=legend_fs, framealpha=1.0)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)


#########################################################################################
plt.subplot(2, 2, 3)
plt.text(-0.3,75.0,"C", weight="bold", fontsize=ylabel_fs)

import tol_colors
light = tol_colors.tol_cset('light')
# same colors used from beNNch 
total_time_colors = [light.light_cyan ,light.pink]
xax = ['NEST', 'NEST GPU main', 'NEST GPU conn', 'GeNN']

# nest
for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["network_construction_time"]["mean"], width=0.25, color = total_time_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_simulate"]["mean"], width=0.25, bottom=nest_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["network_construction_time"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

for i in range(len(ngpu_conn_data)):
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["network_construction_time"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

genn_pos_L = [3.2, 3.45, 3.7]
genn_pos_R = [3.3, 3.55, 3.8]
for i in range(len(genn_data)):
    plt.bar(x=genn_pos_L[i], height=genn_data[i]["network_construction_time"]["mean"], width=0.1, color = total_time_colors[0])
    plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])
    plt.bar(x=genn_pos_R[i], height=genn_data[i]["network_construction_time_nobuild"]["mean"], width=0.1, color = total_time_colors[0])
    plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time_nobuild"]["mean"], color = total_time_colors[1])

plt.ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$' + f'10 s',fontsize=ylabel_fs)
plt.yscale('log')
plt.ylim(1e-1,1e2)
plt.grid(axis='y', which='major', alpha=0.75)
#plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.tick_params(axis="x", length=0)
plt.xticks(ticks=nest_pos + [0.575] + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node ", "2 nodes", "\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.yticks(fontsize=tick_fs)


##############################################################################################

plt.subplot(2, 2, 4)
plt.text(-0.3,72.0,"D", weight="bold", fontsize=ylabel_fs)

for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["network_construction_time"]["mean"], width=0.25, color = total_time_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_simulate"]["mean"], width=0.25, bottom=nest_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["network_construction_time"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

for i in range(len(ngpu_conn_data)):
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["network_construction_time"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])

for i in range(len(genn_data)):
    if i==0:
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time"]["mean"], color = total_time_colors[1], label="Simulation")
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["network_construction_time"]["mean"], width=0.1, color = total_time_colors[0], label="Network construction")
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["network_construction_time_nobuild"]["mean"], width=0.1, color = total_time_colors[0])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time_nobuild"]["mean"], color = total_time_colors[1])
    else:
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["network_construction_time"]["mean"], width=0.1, color = total_time_colors[0])
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time"]["mean"], color = total_time_colors[1])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["network_construction_time_nobuild"]["mean"], width=0.1, color = total_time_colors[0])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["network_construction_time_nobuild"]["mean"], color = total_time_colors[1])


plt.ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$' + f'10 s',fontsize=ylabel_fs)
plt.ylim(0,75)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.tick_params(axis="x", length=0)
plt.xticks(ticks=nest_pos + [0.575] + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node ", "2 nodes", "\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.yticks(fontsize=tick_fs)
plt.legend(fontsize=legend_fs, framealpha=1.0)

plt.tight_layout(w_pad=4.5)

plt.savefig("cm_tot.pdf")
plt.show()


