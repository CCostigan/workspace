#
#
#

import os

class Hello():

    def __init__(self, filename):
        print("TESTING 1...2...3...")

        self.d1 = {
            "a" : 123,
            "b" : 4.56,
            "c" : "Hello",
            "d" : self.function            
        }

        self.d2 = dict(
            a = 123,
            b = 4.56,
            c = "Hello",
            d = self.function
        )
    
    def main(self):
        print("Running main")
        print(self.d1["a"])
        print(self.d2["a"])
        print(self.d1==self.d2)
        self.d2['d']("TESTING")

    def function(self, param):
        print(f"Function called with {param}")


if __name__=='__main__':
    print("Hello (from Python)")
    print("File location: {}".format( __file__ ))    
    h = Hello(__file__)
    h.main()

