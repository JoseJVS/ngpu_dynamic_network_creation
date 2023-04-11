# -*- coding: utf-8 -*-
#
# plot_cm.py

"""

Plotting instructions for cortical microcircuit data.
This script assumes that the data used was generated
by the benchmark.sh script in each model directory.

"""

import matplotlib.pyplot as plt
import tol_colors
import json
from pathlib import Path

tick_fs = 15
legend_fs = 16
ylabel_fs = 18

# Define paths to data directories
nest_path_pg = Path("../data/nest_jureca/microcircuit_benchmarks/poi_gen_benchmark")
nest_path_dc = Path("../data/nest_jureca/microcircuit_benchmarks/dc_input_benchmark")

genn_a100_path = Path("../data/genn_jureca/microcircuit_benchmark")
genn_v100_path = Path("../data/genn_jusuf/microcircuit_benchmark")
genn_2080_path = Path("../data/genn_2080/microcircuit_benchmark")
genn_4090_path = Path("../data/genn_4090/microcircuit_benchmark")

ngpu_main_a100_path_pg = Path("../data/nestgpu_jureca/microcircuit_benchmarks/main_poi_gen_benchmark")
ngpu_main_v100_path_pg = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/main_poi_gen_benchmark")
ngpu_main_2080_path_pg = Path("../data/nestgpu_2080/microcircuit_benchmarks/main_poi_gen_benchmark")
ngpu_main_4090_path_pg = Path("../data/nestgpu_4090/microcircuit_benchmarks/main_poi_gen_benchmark")

ngpu_main_a100_path_dc = Path("../data/nestgpu_jureca/microcircuit_benchmarks/main_dc_input_benchmark")
ngpu_main_v100_path_dc = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/main_dc_input_benchmark")
ngpu_main_2080_path_dc = Path("../data/nestgpu_2080/microcircuit_benchmarks/main_dc_input_benchmark")
ngpu_main_4090_path_dc = Path("../data/nestgpu_4090/microcircuit_benchmarks/main_dc_input_benchmark")

ngpu_conn_a100_path_pg = Path("../data/nestgpu_jureca/microcircuit_benchmarks/conn_poi_gen_benchmark")
ngpu_conn_v100_path_pg = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/conn_poi_gen_benchmark")
ngpu_conn_2080_path_pg = Path("../data/nestgpu_2080/microcircuit_benchmarks/conn_poi_gen_benchmark")
ngpu_conn_4090_path_pg = Path("../data/nestgpu_4090/microcircuit_benchmarks/conn_poi_gen_benchmark")

ngpu_conn_a100_path_dc = Path("../data/nestgpu_jureca/microcircuit_benchmarks/conn_dc_input_benchmark")
ngpu_conn_v100_path_dc = Path("../data/nestgpu_jusuf/microcircuit_benchmarks/conn_dc_input_benchmark")
ngpu_conn_2080_path_dc = Path("../data/nestgpu_2080/microcircuit_benchmarks/conn_dc_input_benchmark")
ngpu_conn_4090_path_dc = Path("../data/nestgpu_4090/microcircuit_benchmarks/conn_dc_input_benchmark")


# Load json benchmark files
nest_benchmark_pg = json.loads(next(nest_path_pg.glob("benchmark*.json")).read_text())
nest_benchmark_dc = json.loads(next(nest_path_dc.glob("benchmark*.json")).read_text())

genn_a100_benchmark = json.loads(next(genn_a100_path.glob("benchmark*.json")).read_text())
genn_v100_benchmark = json.loads(next(genn_v100_path.glob("benchmark*.json")).read_text())
genn_2080_benchmark = json.loads(next(genn_2080_path.glob("benchmark*.json")).read_text())
genn_4090_benchmark = json.loads(next(genn_4090_path.glob("benchmark*.json")).read_text())

ngpu_main_a100_benchmark_pg = json.loads(next(ngpu_main_a100_path_pg.glob("benchmark*.json")).read_text())
ngpu_main_v100_benchmark_pg = json.loads(next(ngpu_main_v100_path_pg.glob("benchmark*.json")).read_text())
ngpu_main_2080_benchmark_pg = json.loads(next(ngpu_main_2080_path_pg.glob("benchmark*.json")).read_text())
ngpu_main_4090_benchmark_pg = json.loads(next(ngpu_main_4090_path_pg.glob("benchmark*.json")).read_text())

ngpu_main_a100_benchmark_dc = json.loads(next(ngpu_main_a100_path_dc.glob("benchmark*.json")).read_text())
ngpu_main_v100_benchmark_dc = json.loads(next(ngpu_main_v100_path_dc.glob("benchmark*.json")).read_text())
ngpu_main_2080_benchmark_dc = json.loads(next(ngpu_main_2080_path_dc.glob("benchmark*.json")).read_text())
ngpu_main_4090_benchmark_dc = json.loads(next(ngpu_main_4090_path_dc.glob("benchmark*.json")).read_text())

ngpu_conn_a100_benchmark_pg = json.loads(next(ngpu_conn_a100_path_pg.glob("benchmark*.json")).read_text())
ngpu_conn_v100_benchmark_pg = json.loads(next(ngpu_conn_v100_path_pg.glob("benchmark*.json")).read_text())
ngpu_conn_2080_benchmark_pg = json.loads(next(ngpu_conn_2080_path_pg.glob("benchmark*.json")).read_text())
ngpu_conn_4090_benchmark_pg = json.loads(next(ngpu_conn_4090_path_pg.glob("benchmark*.json")).read_text())

ngpu_conn_a100_benchmark_dc = json.loads(next(ngpu_conn_a100_path_dc.glob("benchmark*.json")).read_text())
ngpu_conn_v100_benchmark_dc = json.loads(next(ngpu_conn_v100_path_dc.glob("benchmark*.json")).read_text())
ngpu_conn_2080_benchmark_dc = json.loads(next(ngpu_conn_2080_path_dc.glob("benchmark*.json")).read_text())
ngpu_conn_4090_benchmark_dc = json.loads(next(ngpu_conn_4090_path_dc.glob("benchmark*.json")).read_text())

# Specify data selection
nest_benchmark_pg = nest_benchmark_pg[next(iter(nest_benchmark_pg.keys()))]["all_values"]["timers"]
nest_benchmark_dc = nest_benchmark_dc[next(iter(nest_benchmark_dc.keys()))]["all_values"]["timers"]

genn_a100_benchmark = genn_a100_benchmark["timers"]
genn_v100_benchmark = genn_v100_benchmark["timers"]
genn_2080_benchmark = genn_2080_benchmark["timers"]
genn_4090_benchmark = genn_4090_benchmark["timers"]

ngpu_main_a100_benchmark_pg = ngpu_main_a100_benchmark_pg[next(iter(ngpu_main_a100_benchmark_pg.keys()))]["timers"]
ngpu_main_v100_benchmark_pg = ngpu_main_v100_benchmark_pg[next(iter(ngpu_main_v100_benchmark_pg.keys()))]["timers"]
ngpu_main_2080_benchmark_pg = ngpu_main_2080_benchmark_pg[next(iter(ngpu_main_2080_benchmark_pg.keys()))]["timers"]
ngpu_main_4090_benchmark_pg = ngpu_main_4090_benchmark_pg[next(iter(ngpu_main_4090_benchmark_pg.keys()))]["timers"]

ngpu_main_a100_benchmark_dc = ngpu_main_a100_benchmark_dc[next(iter(ngpu_main_a100_benchmark_dc.keys()))]["timers"]
ngpu_main_v100_benchmark_dc = ngpu_main_v100_benchmark_dc[next(iter(ngpu_main_v100_benchmark_dc.keys()))]["timers"]
ngpu_main_2080_benchmark_dc = ngpu_main_2080_benchmark_dc[next(iter(ngpu_main_2080_benchmark_dc.keys()))]["timers"]
ngpu_main_4090_benchmark_dc = ngpu_main_4090_benchmark_dc[next(iter(ngpu_main_4090_benchmark_dc.keys()))]["timers"]

ngpu_conn_a100_benchmark_pg = ngpu_conn_a100_benchmark_pg[next(iter(ngpu_conn_a100_benchmark_pg.keys()))]["timers"]
ngpu_conn_v100_benchmark_pg = ngpu_conn_v100_benchmark_pg[next(iter(ngpu_conn_v100_benchmark_pg.keys()))]["timers"]
ngpu_conn_2080_benchmark_pg = ngpu_conn_2080_benchmark_pg[next(iter(ngpu_conn_2080_benchmark_pg.keys()))]["timers"]
ngpu_conn_4090_benchmark_pg = ngpu_conn_4090_benchmark_pg[next(iter(ngpu_conn_4090_benchmark_pg.keys()))]["timers"]

ngpu_conn_a100_benchmark_dc = ngpu_conn_a100_benchmark_dc[next(iter(ngpu_conn_a100_benchmark_dc.keys()))]["timers"]
ngpu_conn_v100_benchmark_dc = ngpu_conn_v100_benchmark_dc[next(iter(ngpu_conn_v100_benchmark_dc.keys()))]["timers"]
ngpu_conn_2080_benchmark_dc = ngpu_conn_2080_benchmark_dc[next(iter(ngpu_conn_2080_benchmark_dc.keys()))]["timers"]
ngpu_conn_4090_benchmark_dc = ngpu_conn_4090_benchmark_dc[next(iter(ngpu_conn_4090_benchmark_dc.keys()))]["timers"]


simulators=['NEST', 'NEST GPU (offboard)', 'NEST GPU (onboard)', 'GeNN']

ngpu_colors = ['orange', 'cornflowerblue', 'forestgreen', 'lightgreen']
genn_colors = ['yellow', 'steelblue', 'orangered']

# build time plot with different hardware and simulators
fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, figsize = (12,12), tight_layout = True)
ax1.text(-0.1, 1.05, "A", weight="bold", fontsize=ylabel_fs, color='k', transform=ax1.transAxes)
nest_pos = [0.75]
ngpu_conn_pos = [1.2, 1.5, 1.8, 2.1]
genn_pos = [2.5, 2.8, 3.1, 3.4]
nest_data = [nest_benchmark_pg]
ngpu_main_data = [ngpu_main_v100_benchmark_pg, ngpu_main_a100_benchmark_pg, ngpu_main_2080_benchmark_pg, ngpu_main_4090_benchmark_pg]
ngpu_conn_data = [ngpu_conn_v100_benchmark_pg, ngpu_conn_a100_benchmark_pg, ngpu_conn_2080_benchmark_pg, ngpu_conn_4090_benchmark_pg]
genn_data = [genn_v100_benchmark, genn_a100_benchmark, genn_2080_benchmark, genn_4090_benchmark]

for i in range(len(nest_data)):
    ax1.bar(x=nest_pos[i], height=nest_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    ax1.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.2, bottom=nest_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    ax1.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.2, bottom=nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    ax1.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], width=0.2, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    ax1.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], yerr=nest_data[i]["time_construct"]["std"],width=0.2, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data)):
    ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(genn_data)):
    ax1.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
    ax1.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
    ax1.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])
    ax1.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

ax1.set_xticks(ticks=nest_pos + ngpu_conn_pos + [1.65] + genn_pos + [2.95])
ax1.set_xticklabels(labels=[r"2$\times$64 cores" + "\nNEST 3.3 (CPU)", "V100", "A100", "2080Ti", "4090", "\nNEST GPU (onboard)", "V100", "A100", "2080Ti", "4090", "\nGeNN 4.8.0"], fontsize=tick_fs)
ax1.set_ylim(1e-4,1e2)
ax1.set_yscale('log')
ax1.set_ylabel('Network construction [s]', fontsize=ylabel_fs)
ax1.tick_params(labelsize=tick_fs)
ax1.tick_params(axis="x", length=0)
ax1.grid(axis='y', which='major', alpha=0.75)


################################################################
ax2.text(-0.1, 1.05, "B", weight="bold", fontsize=ylabel_fs, color='k', transform=ax2.transAxes)

for i in range(len(nest_data)):
    ax2.bar(x=nest_pos[i], height=nest_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    ax2.bar(x=nest_pos[i], height=nest_data[i]["time_create"]["mean"], width=0.2, bottom=nest_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    ax2.bar(x=nest_pos[i], height=nest_data[i]["time_connect"]["mean"], width=0.2, bottom=nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    ax2.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], width=0.2, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    ax2.bar(x=nest_pos[i], height=nest_data[i]["time_calibrate"]["mean"], yerr=nest_data[i]["time_construct"]["std"],width=0.2, bottom=nest_data[i]["time_connect"]["mean"]+nest_data[i]["time_initialize"]["mean"]+nest_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data)):
    if i == 0:
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0], label = "Initialization")
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1], label = "Node creation")
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2], label = "Node connection")
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3], label = "Calibration")
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
        ax2.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(genn_data)):
    if i==0:
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0], label="Model\ndefinition")
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1], label="Loading")
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2], label="Building")
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_model_def"]["mean"], width=0.2, color = genn_colors[0])
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_load"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"], color = genn_colors[1])
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = genn_colors[2])
        ax2.bar(x=genn_pos[i], height=genn_data[i]["time_build"]["mean"], yerr=genn_data[i]["time_construct"]["std"], width=0.2, bottom=genn_data[i]["time_model_def"]["mean"]+genn_data[i]["time_load"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

ax2.set_xticks(ticks=nest_pos + ngpu_conn_pos + [1.65] + genn_pos + [2.95])
ax2.set_xticklabels(labels=[r"2$\times$64 cores" + "\nNEST 3.3 (CPU)", "V100", "A100", "2080Ti", "4090", "\nNEST GPU (onboard)", "V100", "A100", "2080Ti", "4090", "\nGeNN 4.8.0"], fontsize=tick_fs)
ax2.tick_params(labelsize=tick_fs)
ax2.tick_params(axis="x", length=0)
ax2.set_ylabel('Network construction [s]', fontsize=ylabel_fs)
ax2.legend(title="Network construction phases", ncol=2, fontsize=legend_fs, title_fontsize=legend_fs, framealpha=1.0)
ax2.grid(axis='y', which='major', alpha=0.75)
ax2.grid(axis='y', which='minor', linestyle='--', alpha=0.5)

plt.savefig("cm_net_constr.pdf")


#########################################################################################
plt.figure(2, figsize=(12, 6), dpi=300)
light = tol_colors.tol_cset('light')
med_constr = tol_colors.tol_cset('medium-contrast')
vibrant = tol_colors.tol_cset('vibrant')
# poisson_generator, dc_input, GeNN
total_time_colors = [med_constr.light_red, med_constr.dark_red, vibrant.magenta]
# same colors used from beNNch 
xax = ['NEST', 'NEST GPU (offboard)', 'NEST GPU (onboard)', 'GeNN']

# simulation time [s]
sim_time = 10.0

nest_pos = [0.75]; nest_pos_L = [0.7]; nest_pos_R = [0.8]
#ngpu_main_pos = [1.2, 1.5, 1.8, 2.1]; ngpu_main_pos_L = [1.15, 1.45, 1.75, 2.05]; ngpu_main_pos_R = [1.25, 1.55, 1.85, 2.15]
#ngpu_conn_pos = [2.5, 2.8, 3.1, 3.4]; ngpu_conn_pos_L = [2.45, 2.75, 3.05, 3.35]; ngpu_conn_pos_R = [2.55, 2.85, 3.15, 3.45]
ngpu_conn_pos = [1.2, 1.5, 1.8, 2.1]; ngpu_conn_pos_L = [1.15, 1.45, 1.75, 2.05]; ngpu_conn_pos_R = [1.25, 1.55, 1.85, 2.15]
#genn_pos = [3.8, 4.1, 4.4, 4.7]
genn_pos = [2.5, 2.8, 3.1, 3.4]
nest_data_L = [nest_benchmark_pg]
nest_data_R = [nest_benchmark_dc]
ngpu_main_data_L = [ngpu_main_v100_benchmark_pg, ngpu_main_a100_benchmark_pg, ngpu_main_2080_benchmark_pg, ngpu_main_4090_benchmark_pg]
ngpu_main_data_R = [ngpu_main_v100_benchmark_dc, ngpu_main_a100_benchmark_dc, ngpu_main_2080_benchmark_dc, ngpu_main_4090_benchmark_dc]
ngpu_conn_data_L = [ngpu_conn_v100_benchmark_pg, ngpu_conn_a100_benchmark_pg, ngpu_conn_2080_benchmark_pg, ngpu_conn_4090_benchmark_pg]
ngpu_conn_data_R = [ngpu_conn_v100_benchmark_dc, ngpu_conn_a100_benchmark_dc, ngpu_conn_2080_benchmark_dc, ngpu_conn_4090_benchmark_dc]
genn_data = [genn_v100_benchmark, genn_a100_benchmark, genn_2080_benchmark, genn_4090_benchmark]

for i in range(len(nest_data_L)):
    plt.bar(x=nest_pos_L[i], height=nest_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0])
    plt.bar(x=nest_pos_L[i], height=nest_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=nest_data_L[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
for i in range(len(nest_data_R)):
    plt.bar(x=nest_pos_R[i], height=nest_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1])
    plt.bar(x=nest_pos_R[i], height=nest_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=nest_data_R[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
for i in range(len(ngpu_conn_data_L)):
    if i == 0:
        plt.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0], label="Real-time factor - Poisson generator")
        plt.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_L[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0])
        plt.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_L[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
for i in range(len(ngpu_conn_data_R)):
    if i == 0:
        plt.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1], label="Real-time factor - DC input")
        plt.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_R[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1])
        plt.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_R[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(genn_data)):
    if i==0:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[2], label="Real-time factor - GeNN")
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_simulate"]["mean"]/sim_time, yerr=genn_data[i]["time_simulate"]["std"]/sim_time, width=0.1, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[2])
        plt.bar(x=genn_pos[i], height=genn_data[i]["time_simulate"]["mean"]/sim_time, yerr=genn_data[i]["time_simulate"]["std"]/sim_time, width=0.1, color = "none", capsize=5, error_kw={"elinewidth": 2.25})

plt.ylabel(r'$\mathit{T}_{ wall }\;/\;\mathit{T}_{ model }$ ',fontsize=ylabel_fs)
plt.ylim(0,1.4)
plt.grid(axis='y', which='major', alpha=0.75)
plt.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
plt.tick_params(axis="x", length=0)
plt.xticks(ticks=nest_pos + ngpu_conn_pos + [1.65] + genn_pos + [2.95], labels=[r"2$\times$64 cores" + "\nNEST 3.3 (CPU)", "V100", "A100", "2080Ti", "4090", "\nNEST GPU (onboard)", "V100", "A100", "2080Ti", "4090", "\nGeNN 4.8.0"], fontsize=tick_fs)
plt.yticks(fontsize=tick_fs)
plt.legend(fontsize=legend_fs, framealpha=1.0)

plt.tight_layout()

plt.savefig("cm_overall_real_time_fact.pdf")



fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, figsize = (12,12), tight_layout = True)
ax1.text(-0.1, 1.05, "A", weight="bold", fontsize=ylabel_fs, color='k', transform=ax1.transAxes)
xax = ['NEST GPU (onboard)', 'NEST GPU (offboard)']

ngpu_conn_pos = [1.2, 1.5, 1.8, 2.1]
ngpu_main_pos = [2.6, 2.9, 3.2, 3.5]
for i in range(len(ngpu_main_data)):
    ax1.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
    ax1.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
    ax1.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[2])
    ax1.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = ngpu_colors[3])
    ax1.bar(x=ngpu_main_pos[i], height=ngpu_main_data[i]["time_calibrate"]["mean"], yerr=ngpu_main_data[i]["time_construct"]["std"],width=0.2, bottom=ngpu_main_data[i]["time_connect"]["mean"]+ngpu_main_data[i]["time_initialize"]["mean"]+ngpu_main_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data)):
    if i == 0:
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0], label = "Initialization")
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1], label = "Node creation")
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2], label = "Node connection")
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3], label = "Calibration")
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_initialize"]["mean"], width=0.2, color = ngpu_colors[0])
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_create"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"], color = ngpu_colors[1])
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_connect"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[2])
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = ngpu_colors[3])
        ax1.bar(x=ngpu_conn_pos[i], height=ngpu_conn_data[i]["time_calibrate"]["mean"], yerr=ngpu_conn_data[i]["time_construct"]["std"], width=0.2, bottom=ngpu_conn_data[i]["time_connect"]["mean"]+ngpu_conn_data[i]["time_initialize"]["mean"]+ngpu_conn_data[i]["time_create"]["mean"], color = "none", capsize=5, error_kw={"elinewidth": 2.25})

ax1.set_xticks(ticks= ngpu_main_pos + [1.65] + ngpu_conn_pos + [3.05])
ax1.set_xticklabels(labels=["V100", "A100", "2080Ti", "4090", "\nNEST GPU (onboard)", "V100", "A100", "2080Ti", "4090", "\nNEST GPU (offboard)"], fontsize=tick_fs)
ax1.tick_params(labelsize=tick_fs)
ax1.tick_params(axis="x", length=0)
ax1.set_ylabel('Network construction [s]', fontsize=ylabel_fs)
ax1.set_ylim(1e-4,5e2)
ax1.set_yscale('log')
ax1.legend(title="Network construction phases", ncol=1, fontsize=legend_fs, title_fontsize=legend_fs, framealpha=1.0)
ax1.grid(axis='y', which='major', alpha=0.75)


# simulation time [s]
sim_time = 10.0

ngpu_conn_pos = [1.2, 1.5, 1.8, 2.1]; ngpu_conn_pos_L = [1.15, 1.45, 1.75, 2.05]; ngpu_conn_pos_R = [1.25, 1.55, 1.85, 2.15]
ngpu_main_pos = [2.6, 2.9, 3.2, 3.5]; ngpu_main_pos_L = [2.55, 2.85, 3.15, 3.45]; ngpu_main_pos_R = [2.65, 2.95, 3.25, 3.55]

ngpu_main_data_L = [ngpu_main_v100_benchmark_pg, ngpu_main_a100_benchmark_pg, ngpu_main_2080_benchmark_pg, ngpu_main_4090_benchmark_pg]
ngpu_main_data_R = [ngpu_main_v100_benchmark_dc, ngpu_main_a100_benchmark_dc, ngpu_main_2080_benchmark_dc, ngpu_main_4090_benchmark_dc]
ngpu_conn_data_L = [ngpu_conn_v100_benchmark_pg, ngpu_conn_a100_benchmark_pg, ngpu_conn_2080_benchmark_pg, ngpu_conn_4090_benchmark_pg]
ngpu_conn_data_R = [ngpu_conn_v100_benchmark_dc, ngpu_conn_a100_benchmark_dc, ngpu_conn_2080_benchmark_dc, ngpu_conn_4090_benchmark_dc]

ax2.text(-0.1, 1.05, "B", weight="bold", fontsize=ylabel_fs, color='k', transform=ax2.transAxes)

for i in range(len(ngpu_main_data_L)):
    ax2.bar(x=ngpu_main_pos_L[i], height=ngpu_main_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0])
    ax2.bar(x=ngpu_main_pos_L[i], height=ngpu_main_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_main_data_L[i]["time_simulate"]["std"]/sim_time, width=0.1, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
for i in range(len(ngpu_main_data_R)):
    ax2.bar(x=ngpu_main_pos_R[i], height=ngpu_main_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1])
    ax2.bar(x=ngpu_main_pos_R[i], height=ngpu_main_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_main_data_R[i]["time_simulate"]["std"]/sim_time, width=0.1, color = "none", capsize=5, error_kw={"elinewidth": 2.25})

for i in range(len(ngpu_conn_data_L)):
    if i == 0:
        ax2.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0], label="Real-time factor - Poisson generator")
        ax2.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_L[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        ax2.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[0])
        ax2.bar(x=ngpu_conn_pos_L[i], height=ngpu_conn_data_L[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_L[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
for i in range(len(ngpu_conn_data_R)):
    if i == 0:
        ax2.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1], label="Real-time factor - DC input")
        ax2.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_R[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})
    else:
        ax2.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, width=0.1, color = total_time_colors[1])
        ax2.bar(x=ngpu_conn_pos_R[i], height=ngpu_conn_data_R[i]["time_simulate"]["mean"]/sim_time, yerr=ngpu_conn_data_R[i]["time_simulate"]["std"]/sim_time, width=0.2, color = "none", capsize=5, error_kw={"elinewidth": 2.25})

ax2.set_ylabel(r'$\mathit{T}_{ wall }\;/\;\mathit{T}_{ model }$ ',fontsize=ylabel_fs)
ax2.set_ylim(0,1.4)
ax2.grid(axis='y', which='major', alpha=0.75)
ax2.grid(axis='y', which='minor', linestyle='--', alpha=0.5)
ax2.tick_params(axis="x", length=0)
ax2.set_xticks(ticks=ngpu_conn_pos + [1.65] + ngpu_main_pos + [3.05])
ax2.set_xticklabels(labels=["V100", "A100", "2080Ti", "4090", "\nNEST GPU (onboard)", "V100", "A100", "2080Ti", "4090", "\nNEST GPU (offboard)"], fontsize=tick_fs)
ax2.tick_params(labelsize=tick_fs)
ax2.legend(fontsize=legend_fs, framealpha=1.0, loc='upper left')

plt.savefig("cm_real_time_fact.pdf")



