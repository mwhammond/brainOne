#include <stdlib.h>
#include "objects.h"
#include <ctime>
#include <time.h>

#include "run.h"

#include "code_objects/synapses_pre_push_spikes.h"
#include "code_objects/synapses_post_codeobject.h"
#include "code_objects/spikemonitor_codeobject.h"
#include "code_objects/neurongroup_resetter_codeobject.h"
#include "code_objects/ratemonitor_codeobject.h"
#include "code_objects/synapses_post_initialise_queue.h"
#include "code_objects/poissongroup_group_variable_set_conditional_codeobject.h"
#include "code_objects/statemonitor_codeobject.h"
#include "code_objects/synapses_pre_codeobject.h"
#include "code_objects/poissongroup_thresholder_codeobject.h"
#include "code_objects/synapses_group_variable_set_conditional_codeobject_1.h"
#include "code_objects/neurongroup_thresholder_codeobject.h"
#include "code_objects/synapses_post_push_spikes.h"
#include "code_objects/synapses_synapses_create_codeobject.h"
#include "code_objects/neurongroup_stateupdater_codeobject.h"
#include "code_objects/synapses_pre_initialise_queue.h"
#include "code_objects/synapses_group_variable_set_conditional_codeobject.h"


#include <iostream>
#include <fstream>


        void report_progress(const double elapsed, const double completed, const double duration)
        {
            if (completed == 0.0)
            {
                std::cout << "Starting simulation for duration " << duration << " s";
            } else
            {
                std::cout << completed*duration << " s (" << (int)(completed*100.) << "%) simulated in " << elapsed << " s";
                if (completed < 1.0)
                {
                    const int remaining = (int)((1-completed)/completed*elapsed+0.5);
                    std::cout << ", estimated " << remaining << " s remaining.";
                }
            }

            std::cout << std::endl << std::flush;
        }
        


int main(int argc, char **argv)
{

	brian_start();

	{
		using namespace brian;

		
                
        _run_poissongroup_group_variable_set_conditional_codeobject();
        _run_synapses_synapses_create_codeobject();
        _run_synapses_group_variable_set_conditional_codeobject();
        _run_synapses_group_variable_set_conditional_codeobject_1();
        _run_synapses_post_initialise_queue();
        _run_synapses_pre_initialise_queue();
        magicnetwork.clear();
        magicnetwork.add(&defaultclock, _run_neurongroup_stateupdater_codeobject);
        magicnetwork.add(&defaultclock, _run_neurongroup_thresholder_codeobject);
        magicnetwork.add(&defaultclock, _run_poissongroup_thresholder_codeobject);
        magicnetwork.add(&defaultclock, _run_synapses_post_push_spikes);
        magicnetwork.add(&defaultclock, _run_synapses_post_codeobject);
        magicnetwork.add(&defaultclock, _run_synapses_pre_push_spikes);
        magicnetwork.add(&defaultclock, _run_synapses_pre_codeobject);
        magicnetwork.add(&defaultclock, _run_neurongroup_resetter_codeobject);
        magicnetwork.add(&defaultclock, _run_ratemonitor_codeobject);
        magicnetwork.add(&defaultclock, _run_spikemonitor_codeobject);
        magicnetwork.add(&defaultclock, _run_statemonitor_codeobject);
        magicnetwork.run(100.0, report_progress, 10.0);
        _debugmsg_synapses_post_codeobject();
        
        _debugmsg_spikemonitor_codeobject();
        
        _debugmsg_synapses_pre_codeobject();

	}

	brian_end();

	return 0;
}