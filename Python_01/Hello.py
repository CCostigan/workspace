
import os

class Hello():
    def __init__(self, filename):
        print("TESTING 1...2...3...")
                

if __name__=='__main__':
    print("Hello Mac (from Python)")
    print("File location: {}".format( __file__ ))
    Hello(__file__)

