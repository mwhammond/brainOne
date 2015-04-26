import matplotlib.pyplot as plt
import time
import random
from collections import deque
import numpy as np
import threading
import testHarness
import time
from brian2 import *

ON = 1

class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        testHarness.runit()
        ####### NOTHING BELOW HERE WILL RUN!! ####### 
        
        
        
class plotStuff(threading.Thread):
    def run(self):
        print "plot thread"
       # simulates input from serial port
    

        #a1 = deque([0]*100)
        #ax = plt.axes(xlim=(0, 20), ylim=(0, 10))
        #d = random_gen()
        #line, = plt.plot(a1)
        plt.ion()

        #plt.ylim([0,10])
        plt.show()

        i = 0
        while ON == 1:
            
            testHarness.CURRENT = 1
            print "current to 0.1"
            time.sleep(1)           
            testHarness.CURRENT = 0
            print "current to 0"
            time.sleep(1)
            testHarness.CURRENT = 5
            print "current to 1"
            time.sleep(1)

            
            #print testHarness.statemonHidden[0].vm[0:500]
            
            r = testHarness.statemonHidden[0].vm[:].shape
            print r[0]
            length = r[0]
            start = r[0]-20000
            #a1.appendleft(next(d))
            #datatoplot = a1.pop()
            #line.set_ydata(shape)
            plot(testHarness.statemonHidden[0].vm[start:length])
            plt.draw()
            plt.hold(False)
            #print a1[0]
            i += 1
            #time.sleep(0.1)
            plt.pause(0.0001)  
        

        
        
a = runBrain()
b = plotStuff()

a.start()
b.start()


        
        
            