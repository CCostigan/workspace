


import os
import time
from threading import Thread, Lock



# import logging, os 
# from logging import StreamHandler, FileHandler
# logbase,ext = os.path.splitext(os.path.basename(__file__))
# logging.basicConfig(handlers=[
#     StreamHandler(),
#     FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
# ], format='%(asctime)s %(levelname).3s %(filename)s:%(lineno)-4s %(threadName)s %(message)s'
# , datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
# , level=logging.INFO)

import logging
from logging.config import fileConfig


class ZTest():
    

    
    def __init__(self):
        fileConfig('./res/cfg/alogger.cfg')
        # fileConfig('res/cfg/alogger.cfg')
        # logging.config.fileConfig('res/cfg/alogger.cfg'
        #     , defaults={'logfilename': '/var/log/mylog.log'})
        # create logger
        # 'application' code        

        self.log = logging.getLogger(__file__)

        self.shader_home="res/shaders/"
        self.last_update = time.time()
        self.working=True
        sleeptme = 0.01
        self.log.debug('Debug message')
        time.sleep(sleeptme)
        self.log.info('Info message')
        time.sleep(sleeptme)
        self.log.warning('Warn message')
        time.sleep(sleeptme)
        self.log.error('Error message')
        time.sleep(sleeptme)
        self.log.critical('Critical message')

    def check_files(self, callback, *args):
        filemap = {}
        while self.working:
            for filename in args:
                stats_mt = os.stat(self.shader_home+filename).st_mtime        
                filemap[filename]=stats_mt
                if stats_mt > self.last_update:
                    self.last_update = time.time()
                    callback()
            time.sleep(0.1)


    def thread_callback(self, *args):
        print("GOT HERE thread_callback")

    def start_watch_threads(self, *args):
        self.wt = Thread(target=self.check_files, args=args, daemon=False)
        self.wt.start()

    def stop_threads(self):
        self.working=False
        self.wt.join()
    

if __name__=='__main__':
    print("Starting")
    zt = ZTest()
    zt.start_watch_threads(zt.thread_callback, "shader_vert.glsl", "shader_frag.glsl")
    # input("Press enter\n")             
    zt.stop_threads()
    print("Got here")

#   watch -n 1 python3 src/ZTest.py