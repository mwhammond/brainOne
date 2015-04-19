#include "objects.h"
#include "code_objects/synapses_synapses_create_codeobject.h"
#include<cmath>
#include "brianlib/common_math.h"
#include<stdint.h>
#include<iostream>
#include<fstream>
#include <stdint.h>
#include "synapses_classes.h"

////// SUPPORT CODE ///////
namespace {
 	
 double _rand(int vectorisation_idx)
 {
     return (double)rand()/RAND_MAX;
 }

}

////// HASH DEFINES ///////



void _run_synapses_synapses_create_codeobject()
{	
	using namespace brian;
	///// CONSTANTS ///////////
	const int _numN_incoming = 1;
const int _num_all_post = 1;
int32_t* const _array_synapses__synaptic_post = &_dynamic_array_synapses__synaptic_post[0];
const int _num_synaptic_post = _dynamic_array_synapses__synaptic_post.size();
const int _numN_outgoing = 1000;
const int _num_all_pre = 1000;
int32_t* const _array_synapses__synaptic_pre = &_dynamic_array_synapses__synaptic_pre[0];
const int _num_synaptic_pre = _dynamic_array_synapses__synaptic_pre.size();
	///// POINTERS ////////////
 	
 int32_t * __restrict _ptr_array_synapses_N_incoming = _array_synapses_N_incoming;
 int32_t * __restrict _ptr_array_neurongroup_i = _array_neurongroup_i;
 int32_t * __restrict _ptr_array_synapses__synaptic_post = _array_synapses__synaptic_post;
 int32_t * __restrict _ptr_array_synapses_N_outgoing = _array_synapses_N_outgoing;
 int32_t * __restrict _ptr_array_poissongroup_i = _array_poissongroup_i;
 int32_t * __restrict _ptr_array_synapses__synaptic_pre = _array_synapses__synaptic_pre;


    #include<iostream>
    
    // scalar code
    const int _vectorisation_idx = -1;
 	

	
    for(int _i=0; _i<_num_all_pre; _i++)
	{
		for(int _j=0; _j<_num_all_post; _j++)
		{
		    const int _vectorisation_idx = _j;
   			
   const int32_t _all_post = _ptr_array_neurongroup_i[_j];
   const int32_t _all_pre = _ptr_array_poissongroup_i[_i];
   const int32_t _pre_idx = _all_pre;
   const int32_t _post_idx = _all_post;
   const char _cond = true;
   const int32_t _n = 1;
   const double _p = 1.0;

			// Add to buffer
			if(_cond)
			{
			    if (_p != 1.0) {
			        // We have to use _rand instead of rand to use our rand
			        // function, not the one from the C standard library
			        if (_rand(_vectorisation_idx) >= _p)
			            continue;
			    }
			    for (int _repetition=0; _repetition<_n; _repetition++) {
			        _ptr_array_synapses_N_outgoing[_pre_idx] += 1;
			        _ptr_array_synapses_N_incoming[_post_idx] += 1;
			    	_dynamic_array_synapses__synaptic_pre.push_back(_pre_idx);
			    	_dynamic_array_synapses__synaptic_post.push_back(_post_idx);
                }
			}
		}
	}

	// now we need to resize all registered variables
	const int32_t newsize = _dynamic_array_synapses__synaptic_pre.size();
	_dynamic_array_synapses__synaptic_post.resize(newsize);
	_dynamic_array_synapses__synaptic_pre.resize(newsize);
	_dynamic_array_synapses_Apost.resize(newsize);
	_dynamic_array_synapses_Apre.resize(newsize);
	_dynamic_array_synapses_pre_delay.resize(newsize);
	_dynamic_array_synapses_post_delay.resize(newsize);
	_dynamic_array_synapses_lastupdate.resize(newsize);
	_dynamic_array_synapses_w.resize(newsize);
	// Also update the total number of synapses
	synapses._N_value = newsize;
}


