

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader

shader_home="res/shaders/"

class ShaderLoader():

    def compile_shader(filename, shadertype):
        with open(shader_home+filename, 'r') as source_file:
            shader_src = source_file.readlines()
        # vert_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)
        return compileShader(shader_src, shadertype)


    def load_shader_programs(
            vert_shader_filename, 
            frag_shader_filename,
            geom_shader_filename=None
        ):

        shader_tuple = tuple()
        if vert_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(vert_shader_filename, GL_VERTEX_SHADER),)
        if frag_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(frag_shader_filename, GL_FRAGMENT_SHADER),)
        if geom_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(geom_shader_filename, GL_GEOMETRY_SHADER),)

        shader = compileProgram(*shader_tuple)
        
        print(f"Shaders loaded: {shader}")
        return shader
    
if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")