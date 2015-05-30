import threading
import time
from brian2 import *
import inputgrouptest

figure() 
ON = 1

class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        inputgrouptest.runit()
        ####### NOTHING BELOW HERE WILL RUN!! #######   
        
        
class updateEverything(threading.Thread):
    def run(self):
        print "plot"
        plt.ion()
        plt.show()
        i = 0
        while ON == 1:
            iE, tE = inputgrouptest.spikesE.it
            plot(tE/ms, iE, 'k.') #ms=0.25
            plt.draw()
            plt.hold(False)
            #print a1[0]
            i += 1
            #time.sleep(0.1)
            plt.pause(0.0001) 
        #for x in range (0,100,10):
        #    inputgrouptest.RATEIN = x
        #    time.sleep(0.5)
            
             
        

        
        
a = runBrain()
c = updateEverything()

a.start()
c.start()


### PLOTTING ###





show()