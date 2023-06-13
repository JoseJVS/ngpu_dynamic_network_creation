# -*- coding: utf-8 -*-
#
# configuration file for validation process for the cortical microcircuit model

configuration = {
# number of performed simulations
'nrun': 100,
# absolute paths for simulation output
# output directories should be data{0..nrun-1}
'sim1_path': "/home/gianmarco/ngpu_dynamic_network__creation/data/recording_data/nestgpu_main_set1/",
'sim2_path': "/home/gianmarco/ngpu_dynamic_network__creation/data/recording_data/nestgpu_main_set2/",
'sim3_path': "/home/gianmarco/ngpu_dynamic_network__creation/data/recording_data/nestgpu_conn/",
# distributions boxplot (fring rate, CV ISI and Pearson correlation)
'distributions': ['firing_rate', 'cv_isi', 'correlation'],
'plot_distributions': True,
'distribution_visual': 'violinplot', #['violinplot', 'boxplot']
# pairwise EMD comparison
'emd': True,
'emd_boxplots': True}





