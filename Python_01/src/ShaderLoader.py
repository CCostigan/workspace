

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader
import os
import time
from threading import Thread, Lock

shadermap = {
    "vert": GL_VERTEX_SHADER,
    "frag": GL_FRAGMENT_SHADER,
    "geom": GL_GEOMETRY_SHADER,
    "comp": GL_COMPUTE_SHADER,
    "tess": GL_TESS_CONTROL_SHADER,
    "wtff": GL_REFERENCED_BY_COMPUTE_SHADER,
}

class ShaderLoader():

    shader_home="res/shaders/"

    def __init__(self, shader_home="res/shaders/"):
        self.shader_home = shader_home
        self.last_update = time.time()
        self.checking = True
        # self.args = args
        # self.filemap = ShaderLoader.watcher(*args)

    def compile_shader(self, filename, shadertype):
        with open(self.shader_home+filename, 'r') as source_file:
            shader_src = source_file.readlines()
        return compileShader(shader_src, shadertype)

    # https://www.geeksforgeeks.org/args-kwargs-python/
    def load_shader_progs(self, *args):
        shader_tuple = tuple() 
        for arg in args:
            # print(f"\nARG = {arg} ***")
            for partial in shadermap.keys():
                # print(f"SEARCHING FOR {partial} IN {arg}")
                if partial in arg:
                    # print(f"FOUND {partial} {arg} LOADING AS {shadermap[partial]}")
                    # Adding to a tuple don't forget the comma tup += (blah , )
                    shader_tuple += (self.compile_shader(arg, shadermap[partial]),)
                    break
        shader = compileProgram(*shader_tuple)        
        print(f"Shaders loaded: {shader}")
        return shader



    def check_files(self, *filelist):
        reload = False
        while self.checking:
            for filename in filelist:
                stats_mt = os.stat(self.shader_home+filename).st_mtime        
                if stats_mt > self.last_update:
                    self.last_update = time.time()
                    # self.shaders[0]=self.load_shader_progs(filelist)
                    reload = True
            if reload:
                print(f"Reloading shaders... {filelist}")
                self.load_shader_progs(filelist)

            time.sleep(1.0)

    def start_checking(self, shaders, *filelist):
        print("*** START CHECKING ***")
        self.checking = True
        self.shaders = shaders
        self.checker = Thread(target=self.check_files, args=filelist, daemon=False)
        self.checker.start()

    def stop_checking(self):
        self.checking = False
        if hasattr(self, 'checker'):
            self.checker.join()
        pass


if __name__=='__main__':
    from ShaderLoader import ShaderLoader
    sl = ShaderLoader()
    shader = sl.load_shader_progs(("shader_vert.glsl","shader_frag.glsl"))
    print(f"Shader loader={shader}")