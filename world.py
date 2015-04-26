import threading
import numpy as np
from random import randint
import time
from brian2 import *
import braincore
import snakeGame


duration = '60*seconds'

MY_LOCK = threading.Lock()


SCORE = 0
ON = 1

#MOVE = braincore.MOVE


     
    

class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        braincore.runit()
        ####### NOTHING BELOW HERE WILL RUN!! #######             
      
    
    
class runGame(threading.Thread):
    def run(self):
        #global MOVE
        global ON
        while ON == 1:
            snakeGame.run(6,6)
            

            
            
class updateEverything(threading.Thread):
    def run(self):
        start_time = time.time()
        runningCount1 = 0
        rate1 = 0
        spikesInInterval1 = 0
        
        runningCount2 = 0
        rate2 = 0
        spikesInInterval2 = 0
        
        runningCount3 = 0
        rate3 = 0
        spikesInInterval3 = 0
        
        runningCount4 = 0
        rate4 = 0
        spikesInInterval4 = 0
        
        while ON == 1:
            #print snakeGame.BOARD
            
            # GET BOARD AND SET INPUT
            longboard = np.reshape(snakeGame.BOARD,(36,1))
            longboard[np.greater(longboard, 1)] = 1
            longboard[np.less(longboard, 0)] = 2 #NOT WORKING
            braincore.INPUT = longboard
            
            # OPTMISE WITH MATRIX LATER
            spikesInInterval1 = braincore.OUTPUT[0,0]-runningCount1
            rate1 = spikesInInterval1 / 0.5 # adjust to dynamic interval
            runningCount1 += spikesInInterval1
            
            spikesInInterval2 = braincore.OUTPUT[1,0]-runningCount2
            rate2 = spikesInInterval2 / 0.5 # adjust to dynamic interval
            runningCount2 += spikesInInterval2
            
            spikesInInterval3 = braincore.OUTPUT[2,0]-runningCount3
            rate3 = spikesInInterval3 / 0.5 # adjust to dynamic interval
            runningCount3 += spikesInInterval3
            
            spikesInInterval4 = braincore.OUTPUT[3,0]-runningCount4
            rate4 = spikesInInterval4 / 0.5 # adjust to dynamic interval
            runningCount4 += spikesInInterval4
            
            # GET OUTPUT
            if rate1 > 0:
                snakeGame.MOVE="<Up>"
            elif rate2 > 0:
                snakeGame.MOVE="<Down>"
            elif rate3 > 0:
                snakeGame.MOVE="<Left>"
            elif rate4 > 0:
                snakeGame.MOVE="<Right>"
            else:
                snakeGame.MOVE=""

            
            print snakeGame.MOVE
            time.sleep(0.2)
            
            
#class plotStuff(threading.Thread):
#    def run(self):
#        print "plot thread"
#       # simulates input from serial port
    

        #a1 = deque([0]*100)
        #ax = plt.axes(xlim=(0, 20), ylim=(0, 10))
        #d = random_gen()
        #line, = plt.plot(a1)
#        plt.ion()

        #plt.ylim([0,10])
#        plt.show()

#        i = 0
#        while ON == 1:
            
#            testHarness.CURRENT = 1
#            print "current to 0.1"
#            time.sleep(1)           
#            testHarness.CURRENT = 0
#            print "current to 0"
#            time.sleep(1)
#            testHarness.CURRENT = 5
#            print "current to 1"
#            time.sleep(1)

            
            #print testHarness.statemonHidden[0].vm[0:500]
            
#           r = testHarness.statemonHidden[0].vm[:].shape
#            print r[0]
#            length = r[0]
#            start = r[0]-20000
#            #a1.appendleft(next(d))
#            #datatoplot = a1.pop()
#            #line.set_ydata(shape)
#            plot(testHarness.statemonHidden[0].vm[start:length])
#            plt.draw()
#            plt.hold(False)
#            #print a1[0]
#            i += 1
#            #time.sleep(0.1)
#            plt.pause(0.0001)  
        
        
        
a = runBrain()
b = runGame()
c = updateEverything()

a.start()
b.start()
c.start()