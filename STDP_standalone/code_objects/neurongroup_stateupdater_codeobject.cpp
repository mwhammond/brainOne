#include "objects.h"
#include "code_objects/neurongroup_stateupdater_codeobject.h"
#include<cmath>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>

////// SUPPORT CODE ///////
namespace {
 	

}

////// HASH DEFINES ///////



void _run_neurongroup_stateupdater_codeobject()
{	
	using namespace brian;
	///// CONSTANTS ///////////
	const int _numge = 1;
const int _numv = 1;
const double dt = defaultclock.dt_();
	///// POINTERS ////////////
 	
 double * __restrict _ptr_array_neurongroup_ge = _array_neurongroup_ge;
 double * __restrict _ptr_array_neurongroup_v = _array_neurongroup_v;


	//// MAIN CODE ////////////
	// scalar code
	const int _vectorisation_idx = -1;
 	
 const double _lio_const_1 = - dt;
 const double _lio_const_2 = 0.0 - (-0.06);

	 
	for(int _idx=0; _idx<1; _idx++)
	{
	    // vector code
		const int _vectorisation_idx = _idx;
                
        double ge = _ptr_array_neurongroup_ge[_idx];
        double v = _ptr_array_neurongroup_v[_idx];
        const double _ge = ((_lio_const_1 * ge) / 0.005) + ge;
        const double _v = ((dt * (((-0.074) + (ge * _lio_const_2)) - v)) / 0.01) + v;
        ge = _ge;
        v = _v;
        _ptr_array_neurongroup_ge[_idx] = ge;
        _ptr_array_neurongroup_v[_idx] = v;

	}
}


