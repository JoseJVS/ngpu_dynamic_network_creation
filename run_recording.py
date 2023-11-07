# -*- coding: utf-8 -*-
#
# run_recording.py
# execute with:
#	python3 run_recording.py FILE [--path=PATH] [--seed=SEED] [--algo=ALGO]
#		with FILE the name of the file to output the JSON results.
#		with PATH an optional argument to the path to the directory
#		    where data must be output. Defaults to "$PWD/data".
#		with SEED an optional integer argument for the simulation seed.
#			Defaults to 12345
#		with ALGO an optional integer argument for the number nested loop algorithm to be used.
#			Defaults to 0.
#           Avaiable nested loop algorithms:
#           0: BlockStep
#           1: CumulSum
#           2: Simple
#           3: ParallelInner
#           4: ParallelOuter
#           5: Frame1D
#           6: Frame2D
#           7: Smart1D
#           8: Smart2D

"""
--------------------------------------------------

This is an example script for running the microcircuit model and generating
basic plots of the network activity.

"""

###############################################################################
# Import the necessary modules and start the time measurements.

from stimulus_params import stim_dict
from network_params import net_dict
from sim_params import sim_dict
import network
import nestgpu as ngpu

import numpy as np
from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
from json import dump, dumps
from datetime import datetime

# Get and check file path
parser = ArgumentParser()
parser.add_argument("--file", type=str, default="recording_log")
parser.add_argument("--path", type=str, default=None)
parser.add_argument("--seed", type=int, default=None)
parser.add_argument("--algo", type=int, default=0)
parser.add_argument("--sim_time", type=float, default=10000.)
parser.add_argument("--scale", type=float, default=1.)
args = parser.parse_args()

if args.path is None:
    data_path = Path(sim_dict["data_path"])
else:
    data_path = Path(args.path)
    sim_dict["data_path"] = str(data_path) + "/" # Path to str never ends with /

file_name = args.file + ".json"
file_path = data_path / file_name

assert 0 <= args.algo and args.algo < 9

print(f"Arguments: {args}")

nl_dict = {
        0: "BlockStep",
        1: "CumulSum",
        2: "Simple",
        3: "ParallelInner",
        4: "ParallelOuter",
        5: "Frame1D",
        6: "Frame2D",
        7: "Smart1D",
        8: "Smart2D",
    }

###############################################################################
# Initialize the network with simulation, network and stimulation parameters,
# then create and connect all nodes, and finally simulate.
# The times for a presimulation and the main simulation are taken
# independently. A presimulation is useful because the spike activity typically
# exhibits a startup transient. In benchmark simulations, this transient should
# be excluded from a time measurement of the state propagation phase. Besides,
# statistical measures of the spike activity should only be computed after the
# transient has passed.

sim_dict.update({
    't_presim': 500.,
    't_sim': 1. * args.sim_time,
    'rec_dev': ['spike_detector'],
    'master_seed': datetime.now().microsecond if args.seed is None else args.seed})

net_dict.update({
    'N_scaling': 1. * args.scale,
    'K_scaling': 1. * args.scale,
    'poisson_input': True,
    'V0_type': 'optimized'})

time_start = perf_counter_ns()

net = network.Network(sim_dict, net_dict, stim_dict)

if hasattr(ngpu, "SetNestedLoopAlgo"):
    ngpu.SetNestedLoopAlgo(args.algo)
else:
    print("Cannot set nested loop algorithm in NEST GPU version < 2.0")

time_initialize = perf_counter_ns()

net.create()
time_create = perf_counter_ns()

net.connect()
time_connect = perf_counter_ns()

net.simulate(sim_dict['t_presim'])
time_calibrate = perf_counter_ns()

net.simulate(sim_dict['t_sim'])
time_simulate = perf_counter_ns()

###############################################################################
# Summarize time measurements. Rank 0 usually takes longest because of print
# calls.

time_dict = {
        "time_initialize": time_initialize - time_start,
        "time_create": time_create - time_initialize,
        "time_connect": time_connect - time_create,
        "time_calibrate": time_calibrate - time_connect,
        "time_construct": time_calibrate - time_start,
        "time_simulate": time_simulate - time_calibrate,
        "time_total": time_simulate - time_start,
        }

num_neurons = net.get_network_size()
conf_dict = {
    "nested_loop_algo": nl_dict[args.algo],
    "num_neurons": num_neurons,
    "seed": args.seed,
}

info_dict = {
        "conf": conf_dict,
        "timers": time_dict
    }

with file_path.open("w") as f:
    dump(info_dict, f, indent=4)

print(dumps(info_dict, indent=4))

###############################################################################
# Plot a spike raster of the simulated neurons and a box plot of the firing
# rates for each population.
# For visual purposes only, spikes 100 ms before and 100 ms after the thalamic
# stimulus time are plotted here by default.
# The computation of spike rates discards the presimulation time to exclude
# initialization artifacts.

raster_plot_interval = np.array([stim_dict['th_start'] - 100.0,
                                 stim_dict['th_start'] + 100.0])
firing_rates_interval = np.array([sim_dict['t_presim'],
                                  sim_dict['t_presim'] + sim_dict['t_sim']])
net.evaluate(raster_plot_interval, firing_rates_interval)

