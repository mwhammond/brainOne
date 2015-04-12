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
        while ON == 1:
            print "update operation"
            
            # GET BOARD
            #-> snakeGame.BOARD
            # SCALE VALUES
            # SET INPUT IN BRAINCORE
            # READ OUTPUT FROM BRAINCORE (PAUSE THREAD FOR A MOMENT TO RUN THE BRAIN)
            # PROCESS IN TO A MOVE
            # SEND MOVE TO SNAKE GAME
            
            braincore.INPUT = np.random.rand(10,1) #pull from snake later in snake.BOARD
            ####### SCALE THE BOARD #######
            #get the board from fakesnake
            #set the variable in brain 
            print "play move"
            print "BOARD from snakeGame: {}".format(snakeGame.BOARD) # set in snake namespace
            
            # SEND BOARD
            #MY_LOCK.release()
        
        
a = runBrain()
b = runGame()
c = updateEverything()

a.start()
b.start()
c.start()