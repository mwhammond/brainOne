import threading
class Foo (threading.Thread):
    def __init__(self,x):
        self.__x = x
        threading.Thread.__init__(self)
    def run (self):
        for i in range(100):
            print str(self.__x)

for x in xrange(2):
    Foo(x).start()