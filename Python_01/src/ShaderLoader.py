

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader
import os

shader_home="res/shaders/"

shadermap = {
    "vert": GL_VERTEX_SHADER,
    "frag": GL_FRAGMENT_SHADER,
    "geom": GL_GEOMETRY_SHADER,
    "comp": GL_COMPUTE_SHADER,
    "tess": GL_TESS_CONTROL_SHADER,
    "wtff": GL_REFERENCED_BY_COMPUTE_SHADER,
}

class ShaderLoader():


    def __init__(self, *args):
        self.args = args
        self.filemap = ShaderLoader.watcher(*args)

    def watcher(*args):
        filemap = {}
        for filename in args:
            # dirname = os.path.dirname(filename)
            # basename = os.path.basename(filename)
            stats_mt = os.stat(filename).st_mtime        
            filemap[filename]=stats_mt
        return filemap
    
    def check_shader_changes(self):
        if self.filemap == ShaderLoader.watcher(args):
            pass
        pass

    def compile_shader(filename, shadertype):
        with open(shader_home+filename, 'r') as source_file:
            shader_src = source_file.readlines()
        return compileShader(shader_src, shadertype)

    # https://www.geeksforgeeks.org/args-kwargs-python/
    def load_shader_progs(*args):
        shader_tuple = tuple() # Adding to a tuple don't forget the comma tup += (blah , )
        for arg in args:
            # print(f"\nARG = {arg} ***")
            for partial in shadermap.keys():
                # print(f"SEARCHING FOR {partial} IN {arg}")
                if partial in arg:
                    # print(f"FOUND {partial} {arg} LOADING AS {shadermap[partial]}")
                    shader_tuple += (ShaderLoader.compile_shader(arg, shadermap[partial]),)
                    break
        shader = compileProgram(*shader_tuple)        
        print(f"Shaders loaded: {shader}")
        return shader


if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")