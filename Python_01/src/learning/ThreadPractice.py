



import os
from time import sleep
from threading import Thread, Lock, Event, Condition


class ThreadPractice():

    def __init__(self):
        self.start_threads()
        pass

    def run_function(self, runflags):
        while runflags[0]:
            sleep(1.0)
            print("Processing...")
            pass
        pass

    def start_threads(self):
        self.runflags = [True]
        self.mt = Thread(target=self.run_function, args=[self.runflags], daemon=True)
        self.mt.start()
        pass

    def stop_threads(self):
        self.runflags[0] = False
        self.mt.join()
        pass

if __name__=='__main__':
    ddsu = ThreadPractice()
    input("Press enter to terminate.\n")
    ddsu.stop_threads()
    print("Done...")