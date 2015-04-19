#include "objects.h"
#include "code_objects/synapses_pre_initialise_queue.h"
void _run_synapses_pre_initialise_queue() {
	using namespace brian;
    double* real_delays = &(synapses_pre.delay[0]);
    int32_t* sources = &(synapses_pre.sources[0]);
    const unsigned int n_delays = synapses_pre.delay.size();
    const unsigned int n_synapses = synapses_pre.sources.size();
    synapses_pre.prepare(real_delays, n_delays, sources, n_synapses,
                        synapses_pre.dt);
}
