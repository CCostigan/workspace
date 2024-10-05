

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader

shader_home="res/shaders/"

class ShaderLoader():

    def compile_shader(filename, shadertype):
        with open(shader_home+filename, 'r') as source_file:
            shader_src = source_file.readlines()
        return compileShader(shader_src, shadertype)


    def load_shader_progs(*args):
        shadermap = {
            "vert": GL_VERTEX_SHADER,
            "frag": GL_FRAGMENT_SHADER,
            "geom": GL_GEOMETRY_SHADER,
            "comp": GL_COMPUTE_SHADER,
            "tess": GL_TESS_CONTROL_SHADER,
            "wtff": GL_REFERENCED_BY_COMPUTE_SHADER,
        }
        shader_tuple = tuple() # Adding to atuple don't forget the comma tup += (blah , )
        for arg in args:
            print(f"\nARG = {arg} ***")
            for partial in shadermap.keys():
                print(f"SEARCHING FOR {partial} IN {arg}")
                if partial in arg:
                    print(f"FOUND {partial} {arg} LOADING AS {shadermap[partial]}")
                    shader_tuple += (ShaderLoader.compile_shader(arg, shadermap[partial]),)
                    break
        shader = compileProgram(*shader_tuple)        
        print(f"Shaders loaded: {shader}")
        return shader

    
if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")