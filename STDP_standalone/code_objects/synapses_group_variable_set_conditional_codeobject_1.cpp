#include "objects.h"
#include "code_objects/synapses_group_variable_set_conditional_codeobject_1.h"
#include<math.h>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>


////// SUPPORT CODE ///////
namespace {
 	

}

////// HASH DEFINES ///////



void _run_synapses_group_variable_set_conditional_codeobject_1()
{
	using namespace brian;
	///// CONSTANTS ///////////
	double* const _array_synapses_lastupdate = &_dynamic_array_synapses_lastupdate[0];
const int _numlastupdate = _dynamic_array_synapses_lastupdate.size();
const int32_t N = synapses._N();
	///// POINTERS ////////////
 	
 double * __restrict _ptr_array_synapses_lastupdate = _array_synapses_lastupdate;


	//// MAIN CODE ////////////
	// scalar code
	const int _vectorisation_idx = -1;
 	

 	
 const double _lio_const_1 = 0.0 * 1.0;


	//We add the parallel flag because this is executed outside the main run loop
	
	for(int _idx=0; _idx<N; _idx++)
	{
	    // vector code
		const int _vectorisation_idx = _idx;
  		
  const char _cond = true;

		if (_cond)
		{
                        
            double lastupdate;
            lastupdate = _lio_const_1;
            _ptr_array_synapses_lastupdate[_idx] = lastupdate;

        }
	}
}


