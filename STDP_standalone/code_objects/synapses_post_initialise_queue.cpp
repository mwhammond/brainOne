#include "objects.h"
#include "code_objects/synapses_post_initialise_queue.h"
void _run_synapses_post_initialise_queue() {
	using namespace brian;
    double* real_delays = &(synapses_post.delay[0]);
    int32_t* sources = &(synapses_post.sources[0]);
    const unsigned int n_delays = synapses_post.delay.size();
    const unsigned int n_synapses = synapses_post.sources.size();
    synapses_post.prepare(real_delays, n_delays, sources, n_synapses,
                        synapses_post.dt);
}
