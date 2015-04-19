#include "objects.h"
#include "code_objects/neurongroup_resetter_codeobject.h"
#include<cmath>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>

////// SUPPORT CODE ///////
namespace {
 	

}

////// HASH DEFINES ///////



void _run_neurongroup_resetter_codeobject()
{	
	using namespace brian;
	///// CONSTANTS ///////////
	const int _num_spikespace = 2;
const int _numv = 1;
	///// POINTERS ////////////
 	
 int32_t * __restrict _ptr_array_neurongroup__spikespace = _array_neurongroup__spikespace;
 double * __restrict _ptr_array_neurongroup_v = _array_neurongroup_v;



	const int32_t *_spikes = _ptr_array_neurongroup__spikespace;
	const int32_t _num_spikes = _ptr_array_neurongroup__spikespace[1];

	//// MAIN CODE ////////////	
	// scalar code
	const int _vectorisation_idx = -1;
 	

    
	
	for(int _index_spikes=0; _index_spikes<_num_spikes; _index_spikes++)
	{
	    // vector code
		const int _idx = _spikes[_index_spikes];
		const int _vectorisation_idx = _idx;
                
        double v;
        v = (-0.06);
        _ptr_array_neurongroup_v[_idx] = v;

	}
}


