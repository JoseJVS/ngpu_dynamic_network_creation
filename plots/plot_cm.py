# -*- coding: utf-8 -*-
#
# run_benchmark.py

"""

Plotting instructions for cortical microcircuit data.
This script assumes that the data used was generated
by the benchmark.sh script in each model directory.

"""

import matplotlib.pyplot as plt
import json

from pathlib import Path

tick_fs = 15
legend_fs = 16
ylabel_fs = 18


# Define paths to data directories
nest_path = Path("../data/nest_jureca/microcircuit_benchmarks/poi_gen_benchmark")

genn_a100_path = Path("../data/genn_jureca/microcircuit_benchmark")
genn_v100_path = Path("../data/genn_jusuf/microcircuit_benchmark")
genn_2080_path = Path("../data/genn_jusuf/microcircuit_benchmark") # TODO update when data is available

ngpu_main_a100_path = Path("../data/nestgpu_jureca/microcircuit_benchmarks/main_poi_gen_benchmark")
ngpu_main_v100_path = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/main_poi_gen_benchmark")
ngpu_main_2080_path = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/main_poi_gen_benchmark") # TODO update when data is available

ngpu_conn_a100_path = Path("../data/nestgpu_jureca/microcircuit_benchmarks/conn_poi_gen_benchmark")
ngpu_conn_v100_path = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/conn_poi_gen_benchmark")
ngpu_conn_2080_path = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/conn_poi_gen_benchmark") # TODO update when data is available

# Load json benchmark files
nest_benchmark = json.loads(next(nest_path.glob("benchmark*.json")).read_text())

genn_a100_benchmark = json.loads(next(genn_a100_path.glob("benchmark*.json")).read_text())
genn_v100_benchmark = json.loads(next(genn_v100_path.glob("benchmark*.json")).read_text())
genn_2080_benchmark = json.loads(next(genn_2080_path.glob("benchmark*.json")).read_text())

ngpu_main_a100_benchmark = json.loads(next(ngpu_main_a100_path.glob("benchmark*.json")).read_text())
ngpu_main_v100_benchmark = json.loads(next(ngpu_main_v100_path.glob("benchmark*.json")).read_text())
ngpu_main_2080_benchmark = json.loads(next(ngpu_main_2080_path.glob("benchmark*.json")).read_text())

ngpu_conn_a100_benchmark = json.loads(next(ngpu_conn_a100_path.glob("benchmark*.json")).read_text())
ngpu_conn_v100_benchmark = json.loads(next(ngpu_conn_v100_path.glob("benchmark*.json")).read_text())
ngpu_conn_2080_benchmark = json.loads(next(ngpu_conn_2080_path.glob("benchmark*.json")).read_text())

# Specify data selection
nest_benchmark = nest_benchmark[next(iter(nest_benchmark.keys()))]["all_values"]["timers"]

genn_a100_benchmark = genn_a100_benchmark["timers"]
genn_v100_benchmark = genn_v100_benchmark["timers"]
genn_2080_benchmark = genn_2080_benchmark["timers"]

ngpu_main_a100_benchmark = ngpu_main_a100_benchmark[next(iter(ngpu_main_a100_benchmark.keys()))]["timers"]
ngpu_main_v100_benchmark = ngpu_main_v100_benchmark[next(iter(ngpu_main_v100_benchmark.keys()))]["timers"]
ngpu_main_2080_benchmark = ngpu_main_2080_benchmark[next(iter(ngpu_main_2080_benchmark.keys()))]["timers"]

ngpu_conn_a100_benchmark = ngpu_conn_a100_benchmark[next(iter(ngpu_conn_a100_benchmark.keys()))]["timers"]
ngpu_conn_v100_benchmark = ngpu_conn_v100_benchmark[next(iter(ngpu_conn_v100_benchmark.keys()))]["timers"]
ngpu_conn_2080_benchmark = ngpu_conn_2080_benchmark[next(iter(ngpu_conn_2080_benchmark.keys()))]["timers"]

simulators=['NEST', 'NEST GPU main', 'NEST GPU conn', 'GeNN']
# initialize, create, connect
ngpu_colors = ['orange', 'cornflowerblue', 'forestgreen', 'lightgreen']
# initialize, create, connect, code generation, load
genn_colors = ['yellow', 'steelblue', 'orangered']

# build time plot with different hardware and simulators
plt.figure(1, figsize=(12, 9), dpi=300)
#plt.figure(1)
plt.subplot(2, 1, 1)
plt.text(-0.3,50.0,"A", weight="bold", fontsize=ylabel_fs)
nest_pos = [0.75]
nest_data = [nest_benchmark]
for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_initialize"]["mean"], width=0.25, color = ngpu_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.25, bottom=nest_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.25, bottom=nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], width=0.25, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], yerr=nest_data[i]["time_construct"]["std"],width=0.25, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

ngpu_main_pos = [1.2, 1.5, 1.8]
ngpu_main_data = [ngpu_main_v100_benchmark, ngpu_main_a100_benchmark, ngpu_main_2080_benchmark]
for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], yerr=ngpu_main_data[i]["time_construct"]["std"],width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})


ngpu_conn_pos = [2.2, 2.5, 2.8]
ngpu_conn_data = [ngpu_conn_v100_benchmark, ngpu_conn_a100_benchmark, ngpu_conn_2080_benchmark]
for i in range(len(ngpu_conn_data)):
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

genn_pos = [3.2, 3.5, 3.8]
genn_data = [genn_v100_benchmark, genn_a100_benchmark, genn_2080_benchmark]
for i in range(len(genn_data)):
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])
    plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

plt.xticks(ticks=nest_pos + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.ylim(1e-4,1e2)
plt.yscale('log')
#plt.ylim(0,75)
plt.ylabel('Network construction [s]', fontsize=ylabel_fs)
plt.tick_params(labelsize=tick_fs)
plt.tick_params(axis="x", length=0)
plt.grid(axis='y', which='major', alpha=0.75)
#plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)


################################################################
plt.subplot(2, 1, 2)
plt.text(-0.3,72.0,"B", weight="bold", fontsize=ylabel_fs)

for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_initialize"]["mean"], width=0.25, color = ngpu_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.25, bottom=nest_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.25, bottom=nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], width=0.25, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], yerr=nest_data[i]["time_construct"]["std"],width=0.25, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], yerr=ngpu_main_data[i]["time_construct"]["std"],width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data)):
    if i == 0:
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0], label = "Initialization")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1], label = "Node creation")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2], label = "Node connection")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3], label = "Calibration")
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
        plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(genn_data)):
    if i==0:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0], label="Model\ndefinition")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1], label="Loading")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2], label="Building")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

plt.xticks(ticks=nest_pos + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.ylim(0,75)
plt.tick_params(labelsize=tick_fs)
plt.tick_params(axis="x", length=0)
plt.ylabel('Network construction [s]', fontsize=ylabel_fs)
plt.legend(title="Network construction phases", ncol=2, fontsize=legend_fs, title_fontsize=legend_fs, framealpha=1.0)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)

plt.tight_layout()

plt.savefig("cm_net_constr.pdf")


#########################################################################################
plt.figure(2, figsize=(12, 9), dpi=300)
#plt.text(-0.3,75.0,"A", weight="bold", fontsize=ylabel_fs)

import tol_colors
light = tol_colors.tol_cset('light')
# same colors used from beNNch 
total_time_colors = [light.light_cyan , light.pink, light.light_blue]
xax = ['NEST', 'NEST GPU main', 'NEST GPU conn', 'GeNN']

genn_pos_L = [3.2, 3.45, 3.7]
genn_pos_R = [3.3, 3.55, 3.8]

for i in range(len(nest_data)):
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_construct"]["mean"], width=0.25, color = total_time_colors[0])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_construct"]["mean"], yerr=nest_data[i]["time_construct"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_simulate"]["mean"], width=0.25, bottom=nest_data[i]["time_construct"]["mean"], color = total_time_colors[1])
    plt.bar(x=nest_pos[i], height=nest_data[i]["time_simulate"]["mean"], yerr=nest_data[i]["time_simulate"]["std"], width=0.25, bottom=nest_data[i]["time_construct"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_main_data)):
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_construct"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_construct"]["mean"], yerr=ngpu_main_data[i]["time_construct"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_construct"]["mean"], color = total_time_colors[1])
    plt.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_simulate"]["mean"], yerr=ngpu_main_data[i]["time_simulate"]["std"], width=0.2, bottom=ngpu_main_data[i]["time_construct"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data)):
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_construct"]["mean"], width=0.2, color = total_time_colors[0])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_construct"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_simulate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_construct"]["mean"], color = total_time_colors[1])
    plt.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_simulate"]["mean"], yerr=ngpu_conn_data[i]["time_simulate"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_construct"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(genn_data)):
    if i==0:
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_construct"]["mean"], width=0.1, color = total_time_colors[0], label="Network construction")
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_construct"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["time_construct"]["mean"], color = total_time_colors[1], label="Simulation")
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], yerr=genn_data[i]["time_simulate"]["std"], width=0.1, bottom=genn_data[i]["time_construct"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_construct_no_build"]["mean"], width=0.1, color = total_time_colors[2], label="Network construction\nwithout Building")
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_construct_no_build"]["mean"], yerr=genn_data[i]["time_construct_no_build"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["time_construct_no_build"]["mean"], color = total_time_colors[1])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], yerr=genn_data[i]["time_simulate"]["std"], width=0.1, bottom=genn_data[i]["time_construct_no_build"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_construct"]["mean"], width=0.1, color = total_time_colors[0])
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_construct"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["time_construct"]["mean"], color = total_time_colors[1])
        plt.bar(x=genn_pos_L[i], height=genn_data[i]["time_simulate"]["mean"], yerr=genn_data[i]["time_simulate"]["std"], width=0.1, bottom=genn_data[i]["time_construct"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_construct_no_build"]["mean"], width=0.1, color = total_time_colors[2])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_construct_no_build"]["mean"], yerr=genn_data[i]["time_construct_no_build"]["std"], width=0.25, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], width=0.1, bottom=genn_data[i]["time_construct_no_build"]["mean"], color = total_time_colors[1])
        plt.bar(x=genn_pos_R[i], height=genn_data[i]["time_simulate"]["mean"], yerr=genn_data[i]["time_simulate"]["std"], width=0.1, bottom=genn_data[i]["time_construct_no_build"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

plt.ylabel(r'$T_{\mathrm{wall}}$ [s] for $T_{\mathrm{model}} =$' + f'10 s',fontsize=ylabel_fs)
plt.ylim(0,75)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.tick_params(axis="x", length=0)
plt.xticks(ticks=nest_pos + ngpu_main_pos + ngpu_conn_pos + genn_pos, labels=["1 node\nNEST 3.3", "V100", "A100\nNEST GPU main", "2080Ti", "V100", "A100\nNEST GPU conn", "2080Ti", "V100", "A100\nGeNN 4.8.0", "2080Ti"], fontsize=tick_fs)
plt.yticks(fontsize=tick_fs)
plt.legend(fontsize=legend_fs, framealpha=1.0)

plt.tight_layout()

plt.savefig("cm_tot.pdf")



