PROGRAM = main
SRCS = objects.cpp code_objects/synapses_pre_push_spikes.cpp code_objects/synapses_post_codeobject.cpp code_objects/spikemonitor_codeobject.cpp code_objects/neurongroup_resetter_codeobject.cpp code_objects/ratemonitor_codeobject.cpp code_objects/synapses_post_initialise_queue.cpp code_objects/poissongroup_group_variable_set_conditional_codeobject.cpp code_objects/statemonitor_codeobject.cpp code_objects/synapses_pre_codeobject.cpp code_objects/poissongroup_thresholder_codeobject.cpp code_objects/synapses_group_variable_set_conditional_codeobject_1.cpp code_objects/neurongroup_thresholder_codeobject.cpp code_objects/synapses_post_push_spikes.cpp code_objects/synapses_synapses_create_codeobject.cpp code_objects/neurongroup_stateupdater_codeobject.cpp code_objects/synapses_pre_initialise_queue.cpp code_objects/synapses_group_variable_set_conditional_codeobject.cpp main.cpp network.cpp synapses_classes.cpp run.cpp
H_SRCS = objects.h code_objects/synapses_pre_push_spikes.h code_objects/synapses_post_codeobject.h code_objects/spikemonitor_codeobject.h code_objects/neurongroup_resetter_codeobject.h code_objects/ratemonitor_codeobject.h code_objects/synapses_post_initialise_queue.h code_objects/poissongroup_group_variable_set_conditional_codeobject.h code_objects/statemonitor_codeobject.h code_objects/synapses_pre_codeobject.h code_objects/poissongroup_thresholder_codeobject.h code_objects/synapses_group_variable_set_conditional_codeobject_1.h code_objects/neurongroup_thresholder_codeobject.h code_objects/synapses_post_push_spikes.h code_objects/synapses_synapses_create_codeobject.h code_objects/neurongroup_stateupdater_codeobject.h code_objects/synapses_pre_initialise_queue.h code_objects/synapses_group_variable_set_conditional_codeobject.h network.h synapses_classes.h run.h brianlib/dynamic_array.h brianlib/clocks.h brianlib/common_math.h
OBJS = ${SRCS:.cpp=.o}
CC = @g++
DEBUG = -g
OPTIMISATIONS = -w -O3
CFLAGS = -c -Wno-write-strings $(OPTIMISATIONS) -I. 
LFLAGS = 
DEPS = make.deps

all: executable

# Adds debug flags
debug: CFLAGS += $(DEBUG)
debug: LFLAGS += $(DEBUG)
debug: executable

# Adds -march=native to optimisations, which only works for recent gcc versions
native: OPTIMISATIONS += -march=native
native: executable

.PHONY: all debug native executable clean

executable: $(OBJS) $(DEPS)
	$(CC) $(LFLAGS) $(OBJS) -o $(PROGRAM)

clean:
	rm $(OBJS) $(PROGRAM) $(DEPS)

make.deps: $(SRCS) $(H_SRCS)
	$(CC) $(CFLAGS) -MM $(SRCS) > make.deps
	
ifneq ($(wildcard $(DEPS)), )
include $(DEPS)
endif

%.o : %.cpp
	$(CC) $(CFLAGS) $< -o $@