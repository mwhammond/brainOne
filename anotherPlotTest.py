import matplotlib.pyplot as plt
import time
import random
from collections import deque
import numpy as np
import threading
import inputgrouptest
import time
from brian2 import *

ON = 1

class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        inputgrouptest.runit()
        ####### NOTHING BELOW HERE WILL RUN!! ####### 
        
plt.show()        
        
class plotStuff(threading.Thread):
    def run(self):
        print "plot thread"    

        plt.ion()

        while ON == 1:
            


        
        

        
        
a = runBrain()
b = plotStuff()

a.start()
b.start()


        
        
            