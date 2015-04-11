import pylab
import numpy
rate = 1

x = numpy.linspace(-15,15,100) # 100 linearly spaced numbers
y = numpy.sin(2*numpy.pi*rate*x) # computing the values of sin(x)/x

# compose plot
pylab.plot(x,y) # sin(x)/x
pylab.show() # show the plot