#include "objects.h"


#include "code_objects/synapses_pre_push_spikes.h"
#include<math.h>
#include<stdint.h>
#include "brianlib/common_math.h"

void _run_synapses_pre_push_spikes()
{
	using namespace brian;
    ///// CONSTANTS ///////////
	const int _num_spikespace = 1001;
	///// POINTERS ////////////
        
    int32_t * __restrict _ptr_array_poissongroup__spikespace = _array_poissongroup__spikespace;


    //// MAIN CODE ////////////
	// we do advance at the beginning rather than at the end because it saves us making
	// a copy of the current spiking synapses
	synapses_pre.advance();
	synapses_pre.push(_ptr_array_poissongroup__spikespace, _ptr_array_poissongroup__spikespace[_num_spikespace-1]);
	//synapses_pre.queue->peek();
}
