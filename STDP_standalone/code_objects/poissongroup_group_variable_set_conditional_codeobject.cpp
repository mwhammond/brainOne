#include "objects.h"
#include "code_objects/poissongroup_group_variable_set_conditional_codeobject.h"
#include<math.h>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>


////// SUPPORT CODE ///////
namespace {
 	

}

////// HASH DEFINES ///////



void _run_poissongroup_group_variable_set_conditional_codeobject()
{
	using namespace brian;
	///// CONSTANTS ///////////
	const int _numrates = 1000;
	///// POINTERS ////////////
 	
 double * __restrict _ptr_array_poissongroup_rates = _array_poissongroup_rates;


	//// MAIN CODE ////////////
	// scalar code
	const int _vectorisation_idx = -1;
 	

 	
 const double _lio_const_1 = 15.0 * 1.0;


	//We add the parallel flag because this is executed outside the main run loop
	
	for(int _idx=0; _idx<1000; _idx++)
	{
	    // vector code
		const int _vectorisation_idx = _idx;
  		
  const char _cond = true;

		if (_cond)
		{
                        
            double rates;
            rates = _lio_const_1;
            _ptr_array_poissongroup_rates[_idx] = rates;

        }
	}
}


