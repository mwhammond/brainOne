from brian2 import *
#import snake as snake
import numpy as np
import time


# initiate network


# Define layers ##################################################
inputStart = 0
inputEnd = 31
hidden1Start = 32
hidden1End = 39
hidden2Start = 40
hidden2End = 47
outputStart = 48
outputEnd = 52

duration = 100*ms

# Parameters
boardRows = 6
boardCols = 6
inputNeurons = boardRows*boardCols
hidden1Neurons = inputNeurons/4
hidden2Neurons = 16
outputNeurons = 4

# Parameters

N = 5000
Vr = 10*mV
theta = 20*mV
tau = 20*ms
delta = 2*ms
taurefr = 2*ms
duration = .1*second
C = 1000
sparseness = float(C)/N
J = .1*mV
muext = 25*mV
sigmaext = 1*mV

we = 6*nS  # excitatory synaptic weight
wi = 67*nS  # inhibitory synaptic weight

# The model


# The model #######################################################
eqs = """
dV/dt = (-V+muext + sigmaext * sqrt(tau) * xi)/tau : volt
"""

#inputGroup = NeuronGroup(inputNeurons, eqs, 
#                    threshold='v > -20*mV',
#                    refractory=3*ms,
#                    method='exponential_euler')

indices = array([0])
times = array([50])*ms

inputGroup = SpikeGeneratorGroup(inputNeurons, indices, times)


hidden1Group = NeuronGroup(hidden1Neurons, eqs,
                    threshold='V>theta',
                    reset='V=Vr', refractory=taurefr)


hidden2Group = NeuronGroup(hidden2Neurons, eqs,
                    threshold='V>theta',
                    reset='V=Vr', refractory=taurefr)


outputGroup = NeuronGroup(outputNeurons , eqs,
                    threshold='V>theta',
                    reset='V=Vr', refractory=taurefr)


##LEFT IT AT: LOOKS LIKE ANSWER IS IN NETWORK CUSTOM FUCNTION ON THE HELP STIMULATION PAGE

# Set up connections ###############################################

# Converging code (i.e. first 4 to 1 cell in next layer)

S1 = Synapses(inputGroup, hidden1Group, pre='V += -J')
convergence = inputNeurons/hidden1Neurons
for i in range(0, inputNeurons, convergence):
    S1.connect(list(range(i,i+convergence)),i/convergence) 
    
# connect to all    
S2 = Synapses(hidden1Group, hidden2Group, pre='V += -J')
convergence = hidden1Neurons/hidden2Neurons
for i in range(0, hidden1Neurons):
    S2.connect([i],np.arange(hidden2Neurons)) 


S3 = Synapses(hidden2Group, outputGroup, pre='V += -J')
convergence = hidden2Neurons/outputNeurons
for i in range(0, hidden2Neurons, convergence):
    S3.connect(list(range(i,i+convergence)),i/convergence) 


#S1.w = 'rand()' # j is index of postsynaptic cell
#S2.w = 'rand()' # j is index of postsynaptic cell
#S3.w = 'rand()' # j is index of postsynaptic cell

spikemon1 = SpikeMonitor(inputGroup)
spikemon2 = SpikeMonitor(hidden1Group)
spikemon3 = SpikeMonitor(hidden2Group)
spikemon4 = SpikeMonitor(outputGroup)
trace = StateMonitor(hidden1Group, 'V', record=[0, 4, 7])


board = np.zeros((boardRows,boardCols), dtype=float)
board[2,2] = 40
board[3,2] = 40
board[3,3] = 40
board[3,4] = 40
board[3,5] = 40
board[5,5] = 60 # apple
boardInput = np.reshape(board,(boardRows*boardCols)) #MAKE DYNAMIC!!
# SHOULD THESE ACTUALLY BE FREQUENCIES?
#inputGroup.v[0:36] = boardInput
#G.v0 = 'i*v0_max/(N-1)'

#inputGroup.v = 'El + (randn() * 5 - 5)*mV'
#inputGroup.ge = '(randn() * 1.5 + 4) * 10.*nS'
#inputGroup.gi = '(randn() * 12 + 20) * 10.*nS'

run(100*ms) #NEXT APPLY ARRAY - AS SPIKE EVENTS, SAVE STATE, ITTERATE

# Monitoring #######################################################



def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    


figure()
subplot(231)
plot(spikemon1.t/ms, spikemon1.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(232)
plot(spikemon2.t/ms, spikemon2.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(233)
plot(spikemon3.t/ms, spikemon3.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(234)
plot(spikemon4.t/ms, spikemon4.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')

subplot(235)
plot(trace.t/ms, trace[0].V/mV)
plot(trace.t/ms, trace[4].V/mV)
plot(trace.t/ms, trace[7].V/mV)
xlabel('t (ms)')
ylabel('v (mV)')

#visualise_connectivity(S1)
#visualise_connectivity(S2)
#visualise_connectivity(S3)
show(block=True)

# initiate game ####################################################

#root = snake.run(boardRows,boardCols,group)

# in game methods ##################################################

def move(N,boardMatrix):

    # translate board in to specific input
    run(duration)
    
    # plot ############################
    plot(monitor.t/ms, monitor.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')
    show()
    ###################################

    return N, output #output is 1x4 array (up, down, left right)











