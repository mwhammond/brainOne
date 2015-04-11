import numpy as np
import matplotlib.pyplot as plt

plt.ion()
plt.fig, ax = plt.subplots(2, 3)
plt.fig.tight_layout()


#for r in range(0,rows):
    #for c in range(0, cols):
       # ax[r,c].set_xlim([0,15])
        #ax[r,c].set_ylim([0,10])

ax[0,0].set_title("Voltages")
ax[0,1].set_title("Fire")
ax[0,2].set_title("Buffer")
ax[1,0].set_title("W1")
ax[1,1].set_title("W2")





################### Network class ####################

class network(object):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols 
        self.leak = 0.2
        self.rectify = 0.5
        self.decayConstant = 0.2 #voltage removed per step
        self.inflowConstant = 0.5 #voltage added per step
        self.threshold = 1
        self.maxInputBuffer = 2
        self.maxVoltage = 2
        self.W1 = np.random.randn(self.rows,self.rows) # also defines connections, initiate randomly
        self.W1 = np.absolute(self.W1)
        self.W2 = np.random.randn(self.rows,self.rows) # also defines connections, initiate randomly
        self.W2 = np.absolute(self.W2)
        self.Voltages = np.zeros((self.rows,self.cols), dtype=float) # initiate at same value
        self.Thresholds = np.full((self.rows,self.cols),self.threshold, dtype=float)# initiate at same value
        self.InputBuffer = np.zeros((self.rows,self.cols), dtype=float) # array of voltages amounts for each neuron 
    
    
    def simmulateInput(self,netInput):
        self.Voltages[:,0] = netInput

 
    def setVoltages(self):
        self.InputBuffer
        voltagesToAdd = self.InputBuffer*self.inflowConstant
        self.VoltageBelowMax = np.less(self.Voltages, self.maxVoltage)
        self.VoltageBelowMax=self.VoltageBelowMax.astype(dtype=int)
        voltagesToAdd=voltagesToAdd*self.VoltageBelowMax
        self.Voltages = self.Voltages+voltagesToAdd
        self.InputBuffer = self.InputBuffer-voltagesToAdd
          
        #### decay ####
        
        self.VoltageAboveZero = np.greater(self.Voltages, 0)
        self.VoltageAboveZero=self.VoltageAboveZero.astype(dtype=int)
        self.toDecay=self.VoltageAboveZero*self.decayConstant
        self.Voltages = self.Voltages-self.toDecay
        
    
    def fireCells(self):
        
        for i in range(0,self.cols-1):
            self.atThreshold = np.greater(self.Voltages, self.Thresholds)
            self.InputBufferCol = np.dot(self.atThreshold[:,i].T.astype(dtype=int), self.W1)#<<<<------CHANGE
            self.InputWithRoom = np.less(self.InputBuffer[:,i+1], self.maxInputBuffer)
            self.InputBufferCol = self.InputBufferCol*self.InputWithRoom
            self.InputBuffer[:,i+1] = self.InputBufferCol
        
               
    def readOutput(self):
        return self.atThreshold[:,self.cols-1]
    
    

           
############### End network class ##############

    

def initiateNetwork(rows, cols):    
    return network(rows, cols)

    
def step(N, boardMatrix): 
    scaledBoard = (boardMatrix/float(np.amax(boardMatrix)))*2
    ##########  INPUT ########### 
    #RESHAPE THE BOARD IN TO A ROW
    #N.netInput[0] = np.random.randint(1,10)
    #N.netInput[1] = np.random.randint(1,10)
    #N.netInput[2] = np.random.randint(1,10)
    
    N.simmulateInput(np.reshape(scaledBoard,(N.rows))) #DONT LEAVE THIS AS A FIXED NUMBER <<-----------------
    


    
    N.setVoltages()
    N.fireCells()
    output = N.readOutput()
    
    ######### OUTPUT ###########
    
    ######### PLOTTING ###########

        
    ax[0,0].imshow(N.Voltages, interpolation='none', vmin=0, vmax=5)
    ax[0,1].imshow(N.atThreshold, interpolation='none', vmin=0, vmax=1)
    ax[0,2].imshow(N.InputBuffer, interpolation='none', vmin=0, vmax=5)
    ax[1,0].imshow(N.W1, interpolation='none')
    ax[1,1].imshow(N.W2, interpolation='none')
    
    plt.pause(0.001)
    #for c in range(0, N.cols):
    #    for r in range(0, N.rows):
    #        if N.timeStep > 15:
    #            ax[r,c].set_xlim([N.timeStep-15,N.timeStep])
    #            ax[r,c].scatter(k,N.Voltages[r,c])
    #            ax[r,c].plot([k-15, k], [N.threshold, N.threshold], 'r-', lw=1)
    plt.show(block=False)
     
    return N, output

   
    


        
        
    



