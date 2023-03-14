import sys
import ctypes
import nestgpu as ngpu
from random import randrange

if len(sys.argv) != 2:
    print ("Usage: python %s n_neurons" % sys.argv[0])
    quit()
    
order = int(sys.argv[1])//5

ngpu.SetTimeResolution(1.0)

recording = True
plotting = True

print("Building ...")

ngpu.SetRandomSeed(1234) # seed for GPU random numbers

sim_time = 10.0 # simulation time in seconds

n_receptors = 2

NE = 4 * order       # number of excitatory neurons
NI = 1 * order       # number of inhibitory neurons
n_neurons = NE + NI  # number of neurons in total
print("Neurons: {}".format(n_neurons))

CE = 80     # number of excitatory synapses per neuron
CI = CE//4  # number of inhibitory synapses per neuron

fact=0.42
Wex = 0.5*fact
Win = -3.5*fact

poiss_rate = 50.0
poiss_weight = 13.6

# create poisson generator
pg = ngpu.Create("poisson_generator", n_neurons)
ngpu.SetStatus(pg, "rate", poiss_rate)

# Create n_neurons neurons with n_receptor receptor ports
exc_neuron = ngpu.Create("izhikevich_psc_exp_2s", NE, n_receptors)
inh_neuron = ngpu.Create("izhikevich_psc_exp_2s", NI, n_receptors)

exc_params = {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0}
inh_params = {"a": 0.1, "b": 0.2, "c": -65.0, "d": 2.0}
ngpu.SetStatus(exc_neuron, exc_params)
ngpu.SetStatus(inh_neuron, inh_params)

if recording:
    N_max_spike_times = 100000
    ngpu.ActivateRecSpikeTimes(exc_neuron, N_max_spike_times)
    ngpu.ActivateRecSpikeTimes(inh_neuron, N_max_spike_times)

# Excitatory connections
# connect excitatory neurons to port 0 of all neurons
# normally distributed delays, weight Wex and CE connections per neuron
exc_conn_dict={"rule": "fixed_indegree", "indegree": CE}
exc_syn_dict={"weight": Wex, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 5.0}, "receptor":0}
ngpu.Connect(exc_neuron, exc_neuron, exc_conn_dict, exc_syn_dict)
ngpu.Connect(exc_neuron, inh_neuron, exc_conn_dict, exc_syn_dict)

# Inhibitory connections
# connect inhibitory neurons to port 1 of all neurons
# normally distributed delays, weight Win and CI connections per neuron
inh_conn_dict={"rule": "fixed_indegree", "indegree": CI}
inh_syn_dict={"weight": Win, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 5.0}, "receptor":1}

ngpu.Connect(inh_neuron, exc_neuron, inh_conn_dict, inh_syn_dict)
ngpu.Connect(inh_neuron, inh_neuron, inh_conn_dict, inh_syn_dict)

#connect poisson generator to port 0 of all neurons
pg_conn_dict={"rule": "one_to_one"}
pg_syn_dict={"weight": poiss_weight, "delay": {"distribution": "normal_clipped", "high": 20.0, "low": 1.0, "mu": 10.0, "sigma": 5.0}, "receptor":0}

ngpu.Connect(pg[0:NE], exc_neuron, pg_conn_dict, pg_syn_dict)
ngpu.Connect(pg[NE:n_neurons], inh_neuron, pg_conn_dict, pg_syn_dict)

ngpu.Simulate(sim_time*1000.0)


if recording:
    import numpy as np

    exc_spike_times = ngpu.GetRecSpikeTimes(exc_neuron)
    inh_spike_times = ngpu.GetRecSpikeTimes(inh_neuron)
    # getting firing rate
    frE = np.zeros(NE)
    frI = np.zeros(NI)
    for i in range(len(exc_spike_times)):
        frE[i] = len(exc_spike_times[i])/(sim_time)
    for i in range(len(inh_spike_times)):
        frI[i] = len(inh_spike_times[i])/(sim_time)

    fr = np.concatenate((frE, frI))

    print("Mean firing rate [EXC]: {} +/- {} Hz".format(np.mean(frE), np.std(frE)))
    print("Mean firing rate [INH]: {} +/- {} Hz".format(np.mean(frI), np.std(frI)))
    print("Mean firing rate [TOT]: {} +/- {} Hz".format(np.mean(fr), np.std(fr)))

    if plotting:
        import matplotlib.pyplot as plt
        # raster plot of the spiking activity
        plt.figure()
        for i in range(len(exc_spike_times)):
            plt.plot(exc_spike_times[i], [i for j in range(len(exc_spike_times[i]))], ".", color="b")
        for i in range(len(inh_spike_times)):
            plt.plot(inh_spike_times[i], [i+NE for j in range(len(inh_spike_times[i]))], ".", color="r")
        plt.show()
