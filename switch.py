import threading
import testHarness
import time
from brian2 import *
import matplotlib.pyplot as plt

CURRENT = 0
ON=1

# Start interactive mode

 


class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        testHarness.runit()
        ####### NOTHING BELOW HERE WILL RUN!! #######             
        
    
    
class runGame(threading.Thread):
    def run(self):
        global CURRENT
        plt.ion()
        
        while ON == 1:
            testHarness.CURRENT=1
            time.sleep(0.1)
            testHarness.CURRENT=0
		    #time.sleep(0.3)
            
            
            vm = testHarness.statemonHidden[0].vm[:]
            for t in testHarness.spikesHidden.t:
                i = int(t / defaultclock.dt)
                vm[i] = 20*mV
                plt.plot(testHarness.statemonHidden.t / ms, vm / mV)
                plt.draw()

        
a = runBrain()
b = runGame()

a.start()
b.start()
