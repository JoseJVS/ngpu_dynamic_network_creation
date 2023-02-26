import sys
import nest
import time


if len(sys.argv) != 2:
    print ("Usage: python %s n_neurons" % sys.argv[0])
    quit()
    
order = int(sys.argv[1])//5

nest.ResetKernel()

nest.SetKernelStatus({"local_num_threads": 16})

start_time = time.time()

time_resolution = 0.1

sim_time = 1000.0

delay = 1.0 # synaptic delay in ms

NE = 4 * order  # number of excitatory neurons
NI = 1 * order  # number of inhibitory neurons
n_neurons = NE + NI   # number of neurons in total

CE = 800  # number of excitatory synapses per neuron
CI = int(CE/4)  # number of inhibitory synapses per neuron


Wex = 0.05

Win = -0.35

neuron_params = {
                 "tau_syn_ex": 1.0,
                 "tau_syn_in": 1.0,
                 "V_reset": -60.0
}


nest.SetKernelStatus({"resolution": time_resolution, "print_time": False,
                      "overwrite_files": True})

print("Building ...")

nest.SetDefaults("aeif_cond_alpha", neuron_params)

nodes_ex = nest.Create("aeif_cond_alpha", NE)
nodes_in = nest.Create("aeif_cond_alpha", NI)

mean_delay = 0.5
std_delay = 0.25
min_delay = 0.1

syn_dict_exc = {"synapse_model": "static_synapse", "weight": Wex,
                "delay": nest.math.redraw(nest.random.normal(mean=mean_delay, std=std_delay), min=min_delay, max=mean_delay+3*std_delay)}

syn_dict_inh = {"synapse_model": "static_synapse", "weight": Win,
                "delay": nest.math.redraw(nest.random.normal(mean=mean_delay, std=std_delay), min=min_delay, max=mean_delay+3*std_delay)}

from numpy import loadtxt
from numpy import arange

pg = nest.Create("poisson_generator")
nest.SetStatus(pg, {"rate": 20000.0})

poiss_delay = 0.2
poiss_weight = 0.37
nest.CopyModel("static_synapse", "poisson_connection",
               {"weight": poiss_weight, "delay": poiss_delay})

nest.Connect(pg, nodes_ex, {'rule': 'all_to_all'}, "poisson_connection")
nest.Connect(pg, nodes_in, {'rule': 'all_to_all'}, "poisson_connection")

conn_params_ex = {'rule': 'fixed_indegree', 'indegree': CE}
nest.Connect(nodes_ex, nodes_ex + nodes_in, conn_params_ex, syn_dict_exc)

conn_params_in = {'rule': 'fixed_indegree', 'indegree': CI}
nest.Connect(nodes_in, nodes_ex + nodes_in, conn_params_in, syn_dict_inh)

# for performance evaluation comment spike recorders and firing rate calculation
#sr = nest.Create("spike_recorder")
#nest.Connect(nodes_ex, sr)

build_time = time.time()

print("Simulating ...")

nest.Simulate(sim_time)

end_time = time.time()

print("Building time     : %.2f s" % (build_time - start_time))
print("Simulation time   : %.2f s" % (end_time - build_time))

#spikes = sr.get("events")
#fr = len(spikes["senders"])/((sim_time/1000.0)*NE)
#print("Firing rate: {} Hz".format(fr))

