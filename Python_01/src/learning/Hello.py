#
#
#

import time
import threading

'''  Logging in Python - According to HAL
Format String Placeholders:
%(asctime)s: Human-readable time when the LogRecord was created.
%(created)f: Time in seconds since the epoch when the LogRecord was created.
%(filename)s: Filename portion of the pathname.
%(funcName)s: Name of the function containing the logging call.
%(levelname)s: Text logging level for the message ('DEBUG', 'INFO', etc.).
%(levelno)d: Numeric logging level for the message (10 for DEBUG, 20 for INFO, etc.).
%(lineno)d: Line number where the logging call was made.
%(message)s: The logged message itself.
%(module)s: Module (name portion of filename).
%(name)s: Name of the logger (useful for filtering).
%(pathname)s: Full pathname of the source file where the logging call was issued.
%(process)d: Process ID.
%(processName)s: Process name.
%(thread)d: Thread ID.
%(threadName)s: Thread name.'''
import logging, os 
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(),
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname).3s %(filename)s:%(lineno)s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.DEBUG)

class Hello():

    def __init__(self, filename):
        self.log = logging.getLogger(__file__)

        self.log.info('TESTING 1...2...3...')

        self.d1 = {
            'a' : 123,
            'b' : 4.56,
            'c' : 'Hello',
            'd' : self.function            
        }

        self.d2 = dict(
            a = 123,
            b = 4.56,
            c = 'Hello',
            d = self.function
        )
    
    def pythonthreadingisgarbage(self, evnt, foo):
        self.log.info(f'pythonthreadingisgarbage called...{foo}')
        while not evnt.is_set():
            time.sleep(1)

    def main(self):
        self.log.info('Running main')
        self.log.info(self.d1['a'])
        self.log.info(self.d2['a'])
        self.log.info(self.d1==self.d2)
        self.d2['d']('TESTING')
        self.evnt = threading.Event()
        t = threading.Thread(target=self.pythonthreadingisgarbage, args=(self.evnt, 'TEST', ))
        self.log.info(t)
        t.start()                
        self.log.info(t)
        time.sleep(4)
        self.log.info(t)
        time.sleep(4)
        self.log.info(t)
        self.done()
        time.sleep(4)
        self.log.info(t)

    def done(self):
        self.evnt.set()

    def function(self, param):
        self.log.info(f'Function called with {param}')


if __name__=='__main__':
    h = Hello(__file__)
    h.log.info('Hello (from Python)')
    h.log.debug('File location: {}'.format( __file__ ))    
    h.log.debug(f'File location: {__file__}')
    h.main()
    input("Press enter when done\n")
    h.done()

