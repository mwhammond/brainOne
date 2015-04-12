import threading
import numpy as np
from random import randint
import time
from brian2 import *
import braincore
import fakeSnake

duration = '60*seconds'

MY_LOCK = threading.Lock()


SCORE = 0

#MOVE = braincore.MOVE


     
    

class runBrain(threading.Thread):
    def run(self):
        # ANYTHING HERE WILL ONLY BE RUN ONCE
        braincore.runit()
        ####### NOTHING BELOW HERE WILL RUN!! #######             
        
class runGame(threading.Thread):
    def run(self):
        #global MOVE
        for i in range(10000):
            
            braincore.INPUT = np.random.rand(10,1) #pull from snake later in snake.BOARD
            ####### SCALE THE BOARD #######
            #get the board from fakesnake
            #set the variable in brain
            
            #MY_LOCK.acquire()
            # PLAY MOVE
            print "play move"
            #if MOVE is not None: 
            print "Printing MOVE from game thread: {}".format(braincore.OUTPUT) # set in snake namespace
            
            # SEND BOARD
            time.sleep(0.2)
            #MY_LOCK.release()
        
        
a = runBrain()
b = runGame()

a.start()
b.start()