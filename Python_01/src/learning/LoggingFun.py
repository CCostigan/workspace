

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
%(threadName)s: Thread name.

We can limit the length of these like so - %(levelname).3s
'''

import logging, sys, os 
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(sys.stdout),  # Console logs to STDERR but what if I want to grep it?
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname).3s %(filename)s:%(lineno)s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.DEBUG)

class JustLearning():
    def __init__(self):
        self.log = logging.getLogger(__file__)        

        self.log.debug("Debug message   - Is this really doing what it should?")
        self.log.info( "Informational   - Thought you might want to know")
        self.log.error("Error message   - Something went wrong, but we're handling it")
        self.log.fatal("Fatal message   - It's hit the fan.  Everybody out.  Run!")

        pass

if __name__== '__main__':
    learn = JustLearning()

