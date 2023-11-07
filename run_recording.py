# -*- coding: utf-8 -*-
#
# run_microcircuit.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

"""PyNEST Microcircuit: Run Simulation
-----------------------------------------

This is an example script for running the microcircuit model and generating
basic plots of the network activity.

"""

###############################################################################
# Import the necessary modules and start the time measurements.

from stimulus_params import stim_dict
from network_params import net_dict
from sim_params import sim_dict
import network
import nest

import numpy as np
from time import perf_counter_ns
from argparse import ArgumentParser
from pathlib import Path
from json import dump, dumps
from datetime import datetime

# Get and check file path
parser = ArgumentParser()
parser.add_argument("--file", type=str, default="benchmark_log")
parser.add_argument("--path", type=str, default=None)
parser.add_argument("--seed", type=int, default=None)
parser.add_argument("--threads", type=int, default=2)
parser.add_argument("--sim_time", type=float, default=10000.)
parser.add_argument("--scale", type=float, default=1.)
args = parser.parse_args()

if args.path is None:
    data_path = Path(sim_dict["data_path"])
else:
    data_path = Path(args.path)
    sim_dict["data_path"] = str(data_path) + "/" # Path to str never ends with /

rank = nest.Rank()
file_name = args.file + f"_rank_{rank}.json"
file_path = data_path / file_name
assert 0 < args.threads

print(f"Arguments: {args}")

###############################################################################
# Initialize the network with simulation, network and stimulation parameters,
# then create and connect all nodes, and finally simulate.
# The times for a presimulation and the main simulation are taken
# independently. A presimulation is useful because the spike activity typically
# exhibits a startup transient. In benchmark simulations, this transient should
# be excluded from a time measurement of the state propagation phase. Besides,
# statistical measures of the spike activity should only be computed after the
# transient has passed.
#
# Benchmark: In contrast to run_microcircuit.py, some default simulation and
# network parameters are here overwritten.


sim_dict.update({
    't_presim': 500.,
    't_sim': 1. * args.sim_time,
    'rec_dev': ['spike_recorder'],
    'rng_seed': datetime.now.microseconds if args.seed is None else args.seed,
    'local_num_threads': args.threads,
    'print_time': False})

net_dict.update({
    'N_scaling': 1. * args.scale,
    'K_scaling': 1. * args.scale,
    'poisson_input': True,
    'V0_type': 'optimized'})

time_start = perf_counter_ns()

net = network.Network(sim_dict, net_dict, stim_dict)
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

###############################################################################
# Query the accumulated number of spikes on each rank.

local_spike_counter = nest.GetKernelStatus('local_spike_counter')
num_neurons = nest.GetKernelStatus('network_size')
rate = 1. * local_spike_counter / num_neurons / (sim_dict['t_presim'] + sim_dict['t_sim']) * 1000

stats_dict = {
    "local_spike_counter": local_spike_counter,
    "rate": rate
}

if args.threads != nest.GetKernelStatus('local_num_threads'):
    print("WARNING: Thread number mismatch")

nprocs = nest.NumProcesses()

conf_dict = {
    "threads": args.threads,
    "procs": nprocs,
    "num_neurons": num_neurons,
    "seed": args.seed,
}
    
info_dict = {
    "rank": rank,
    "conf": conf_dict,
    "stats": stats_dict,
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
