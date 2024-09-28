

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader

class ShaderLoader():

    def load_shader(
            vertex_shader_filename, 
            fragment_shader_filename  ):

        shader_home="res/shaders/"

        with open(shader_home+vertex_shader_filename, 'r') as vertex_file:
            vertex_shader_src = vertex_file.readlines()
        # print(f"Src:{vertex_shader_src}")
        vert_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)


        with open(shader_home+fragment_shader_filename, 'r') as fragment_file:
            fragment_shader_src = fragment_file.readlines()
        # print(f"Src:{fragment_shader_src}")
        frag_shader = compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)    

        print(f"vert_shader:{vert_shader}")
        print(f"frag_shader:{frag_shader}")

        shader = compileProgram(vert_shader,frag_shader)
        return shader
    
if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")