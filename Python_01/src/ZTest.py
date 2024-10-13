
import os
import time
from threading import Thread, Lock

class ZTest():
    
    def __init__(self):
        self.shader_home="res/shaders/"
        self.last_update = time.time()
        self.working=True

    def check_files(self, callback, *args):
        filemap = {}
        while self.working:
            for filename in args:
                stats_mt = os.stat(self.shader_home+filename).st_mtime        
                filemap[filename]=stats_mt
                if stats_mt > self.last_update:
                    self.last_update = time.time()
                    callback()
                else:
                    time.sleep(1.0)


    def thread_callback(self, *args):
        print("GOT HERE thread_callback")

    def start_watch_threads(self, *args):
        self.wt = Thread(target=self.check_files, args=args, daemon=False)
        self.wt.start()

    def stop_threads(self):
        self.working=False
        self.wt.join()
    

if __name__=='__main__':
    zt = ZTest()
    zt.start_watch_threads(zt.thread_callback, "shader_vert.glsl", "shader_frag.glsl")
    input("Press enter\n")             
    zt.stop_threads()
    print("Got here")

