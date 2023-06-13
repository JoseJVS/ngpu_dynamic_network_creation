# -*- coding: utf-8 -*-
#
# run_validation.py
# execute with:
#	python3 run_validation.py

from val_config import configuration
from val_helpers import __get_distributions, __get_distributions_csv, __plot_distributions, __get_emd, __get_emd_csv, __plot_emd

# simulation sets we want to get the distributions from
# Sim 1: set of simulations using NEST GPU main
# Sim 2: set of simulations using NEST GPU main (using different seeds wrt Set 1)
# Sim 3: set of simulations using NEST GPU conn
sim_set = ['Sim 1', 'Sim 2', 'Sim 3']
__get_distributions(set = sim_set)

if(configuration['plot_distributions']):
    # compute the csv files needed to plot the distributions
    # chose the set of simulations to compare with Sim 3 ('Sim 1' or 'Sim 2')
    __get_distributions_csv(simulation = 'Sim 1')
    # chose the dataX set to plot
    __plot_distributions(run_id=0)

if(configuration['emd']):
    # computes emd for the comparisons "Sim 1 - Sim 2" and "Sim 1 - Sim 3"
    __get_emd()
    if(configuration['emd_boxplots']):
        # computes the csv files needed to get the EMD box plots
        __get_emd_csv()
        # plot EMD box plots
        __plot_emd()









