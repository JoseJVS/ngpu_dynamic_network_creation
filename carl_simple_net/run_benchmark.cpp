/*
 * TODO HEADER 
 */

// include CARLsim user interface
#include <carlsim.h>

// include chrono library for headers
#include<chrono>

// include assert library for argument checking
#include <assert.h>

const std::string get_connection_routine(int argc, char* argv[]) {
	if ( argc >= 2 ) {
		const std::string conn_type = argv[1];
		assert( conn_type == "full" || conn_type == "one-to-one" );
		return conn_type;
	} else 
		return "full";
}

int get_pop_size(int argc, char* argv[]) {
	if ( argc >= 3 ) {
		int pop_size = atoi(argv[2]);
		assert(pop_size > 0);
		return pop_size;
	} else
		return 1000;
}

int get_rand_seed(int argc, char* argv[]) {
	if ( argc >= 4 ) {
		int rand_seed = atoi(argv[3]);
		return rand_seed;
	} else
		return 12345;
}

int main(int argc, char* argv[]) {
	// setup benchmark parameters
	const std::string conn_type = get_connection_routine(argc, argv);
	int pop_size = get_pop_size(argc, argv);
	int rand_seed = get_rand_seed(argc, argv);

	auto time_start = std::chrono::high_resolution_clock::now();

	// create CARLsim object
	CARLsim sim("benchmark_construction", GPU_MODE, USER, 0, rand_seed);

	// configure the network
	int g1 = sim.createGroup("pop1", pop_size, EXCITATORY_NEURON, 0, GPU_CORES);
	sim.setNeuronParameters(g1, 0.0f, 0.0f, 0.0f, 0.0f); // RS
	int g2 = sim.createGroup("pop2", pop_size, EXCITATORY_NEURON, 0, GPU_CORES);
	sim.setNeuronParameters(g2, 0.0f, 0.0f, 0.0f, 0.0f); // RS

	sim.connect(g1, g2, conn_type, RangeWeight(1.0f), 1.0f, RangeDelay(1), RadiusRF(-1), SYN_FIXED);
	sim.connect(g2, g1, conn_type, RangeWeight(1.0f), 1.0f, RangeDelay(1), RadiusRF(-1), SYN_FIXED);
	sim.connect(g1, g1, conn_type, RangeWeight(1.0f), 1.0f, RangeDelay(1), RadiusRF(-1), SYN_FIXED);
	sim.connect(g2, g2, conn_type, RangeWeight(1.0f), 1.0f, RangeDelay(1), RadiusRF(-1), SYN_FIXED);

	sim.setConductances(false);

	// build the network
	sim.setupNetwork();

	auto time_construct = std::chrono::high_resolution_clock::now();

	// run the network for 1 milisecond
	sim.runNetwork(0, 1);
	
	auto time_simulate = std::chrono::high_resolution_clock::now();

	auto tt_construct = time_construct - time_start;
	auto tt_simulate = time_simulate - time_construct;

	printf("Time to construct: %li, time to simulate: %li\n", tt_construct.count(), tt_simulate.count());

	return 0;
}
