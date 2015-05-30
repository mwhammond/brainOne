import threading
import inputgrouptest2
import matplotlib.pyplot as plt
from brian2 import *
import time


ON = 1





def brain():
    inputgrouptest2.runit()
    
    

def plot():
    plt.ion()
    RATEIN = 0
    buttons = ["Up", "Down", "Left", "Right"]
    while ON == 1:
        time.sleep(0.1) 
        
# STIMULATE
        
        inputgrouptest2.INPUT = [RATEIN, RATEIN, RATEIN, RATEIN]
        RATEIN += 1
        
# READ OUTPUT
        output = inputgrouptest2.OUTPUT

        if max(output)>0:
            val = output.argmax(axis=0)
            print buttons[val]
        else:
            print "No Move"
            
        
# PLOT        
        
        iE = np.array(inputgrouptest2.iE)
        tE = np.array(inputgrouptest2.tE)
        
        a = tE.shape
        a = a[0]
        if a >100:

            #plt.plot(inputgrouptest.tE[a-1000:a]/ms, inputgrouptest.iE[a-1000:a]/mV, 'k.') #ms=0.25
            plt.plot(inputgrouptest2.tE[:a]/ms, inputgrouptest2.iE[:a]/mV, 'k.') #ms=0.25
            plt.draw()
            plt.hold(False)
            #plt.pause(0.0001) 
            
            
            
# READ STATE / MAKE MOVE
  
print inputgrouptest2.Pe
    

    
if __name__ == '__main__':
    brain = threading.Thread(target=brain)
    plot = threading.Thread(target=plot)

        
    brain.start()
    plot.start()
    
    # only stop plotting once brain has finished its loop
    brain.join()
    if brain.is_alive():
        print nothing
    else:
        plot.join()    
    
    

#def f(conn):
#    while X == 1:
#        conn.send([42, None, 'hello'])
#        conn.close()
        #NEXT KEEP THIS ALIVE WITH A WHILE

#if __name__ == '__main__':
#    parent_conn, child_conn = Pipe()
#    p = Process(target=f, args=(child_conn,))
#    p2 = Process(target=brain)
    
#    p.start()
#    p2.start()
    
    
#    print parent_conn.recv()   # prints "[42, None, 'hello']"
#   # p.join()
#   # p2.join()