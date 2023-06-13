# NEST GPU Validation for Cortical Microcircuit model simulations

Here is presented a fast way for comparing the results in terms of spiking activity between the two versions of NEST GPU for the simulation of the Cortical Microcircuit model (Potjans, 2014). 

The validation takes in input the files of the spike times for the simulations and returns the distributions of firing rate, CV ISI and Pearson correlation for every population of the model. The distributions obtained using the two versions of NEST GPU are shown side by side using box plots or violin plots, and are quantitatively compared using the Earth Mover's Distance (EMD) metric.

## What you need to start the validation

To perform the validation you need 3 sets of ``nrun`` simulations:
- a set NEST GPU simulations with the new method for network construction;
- two sets of the previous version of NEST GPU simulations with different seeds for random number generation.

All the simulations should have enabled the recording of the spikes and should have 500 ms of presimulation and 10000 ms of simulation. The simulations sets should be stored in separate directories, and the results of each simulation of the set should be saved into separate folders (data0, data1, ..., data9).

## Configuration

To set all the steps of the validation process you can edit the Python script ``val_config.py`` which contains all the information needed to perform the validation. You can edit the number of simulations for each set (i.e. ``nrun``), the paths for the simulation directories and boolean parameters that can enable or disable the computation of the distribution plots and the EMD box plots.

## Run validation

To run the validation you should edit the Python script ``run_validation.py``. This script computes first the csv files needed to produce the violin plots and the box plots, and then saves the plots in PDF format. If csv files are already computed, they are directly loaded to produce the plots. If you want to compute again the data needed for the plots you should remove the csv files already produced in the ``csv`` directory.
