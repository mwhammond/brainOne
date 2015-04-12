import threading
import numpy as np
from random import randint
import time
from brian2 import *
import braincore

duration = '60*seconds'

MY_LOCK = threading.Lock()


SCORE = 0
BOARD = np.zeros((3,3))
#MOVE = braincore.MOVE


    


def printHello():
    print "lone print statement"

    
    

class runBrain(threading.Thread):
    def run(self):
        braincore.runit()
        ####### NOTHING BELOW HERE WILL RUN!! #######
        
        #for i in range(1000):
        #inputNeuron = [0,0,0]
        #outputNeuron = [0]
        #MY_LOCK.acquire()
        # SET INPUT FROM BOARD
        #inputNeuron[0] = BOARD[0,0]
        #print "value of board"
        #print inputNeuron[0]
        # GET OUTPUT
        #outputNeuron[0] = randint(0,4)
        #MOVE = outputNeuron[0] 
        #MY_LOCK.release()
            
              
        
class runGame(threading.Thread):
    def run(self):
        global MOVE
        for i in range(10000):
            #MY_LOCK.acquire()
            # PLAY MOVE
            print "play move"
            #if MOVE is not None: 
            print "Printing MOVE from game thread: {}".format(braincore.MOVE) 
            # SEND BOARD
            BOARD = np.random.rand(3,3)
            time.sleep(0.2)
            #MY_LOCK.release()
        
        
a = runBrain()
b = runGame()

a.start()
b.start()