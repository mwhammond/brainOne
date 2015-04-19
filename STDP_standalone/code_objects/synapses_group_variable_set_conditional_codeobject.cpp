#include "objects.h"
#include "code_objects/synapses_group_variable_set_conditional_codeobject.h"
#include<math.h>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>


////// SUPPORT CODE ///////
namespace {
 	
 double _rand(int vectorisation_idx)
 {
     return (double)rand()/RAND_MAX;
 }

}

////// HASH DEFINES ///////



void _run_synapses_group_variable_set_conditional_codeobject()
{
	using namespace brian;
	///// CONSTANTS ///////////
	const int32_t N = synapses._N();
double* const _array_synapses_w = &_dynamic_array_synapses_w[0];
const int _numw = _dynamic_array_synapses_w.size();
	///// POINTERS ////////////
 	
 double * __restrict _ptr_array_synapses_w = _array_synapses_w;


	//// MAIN CODE ////////////
	// scalar code
	const int _vectorisation_idx = -1;
 	

 	


	//We add the parallel flag because this is executed outside the main run loop
	
	for(int _idx=0; _idx<N; _idx++)
	{
	    // vector code
		const int _vectorisation_idx = _idx;
  		
  const char _cond = true;

		if (_cond)
		{
                        
            double w;
            w = _rand(_vectorisation_idx) * 0.01;
            _ptr_array_synapses_w[_idx] = w;

        }
	}
}


