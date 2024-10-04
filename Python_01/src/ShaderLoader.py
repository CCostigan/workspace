

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader

shader_home="res/shaders/"

class ShaderLoader():

    def compile_shader(filename, shadertype):
        with open(shader_home+filename, 'r') as source_file:
            shader_src = source_file.readlines()
        return compileShader(shader_src, shadertype)


    def load_shader_programs(
            vert_shader_filename, 
            frag_shader_filename,
            geom_shader_filename=None,
            comp_shader_filename=None,
            tess_shader_filename=None,
            wtff_shader_filename=None,
        ):

        shader_tuple = tuple() # Adding to atuple don't forget the comma tup += (blah , )
        if vert_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(vert_shader_filename, GL_VERTEX_SHADER),)
        if frag_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(frag_shader_filename, GL_FRAGMENT_SHADER),)
        if geom_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(geom_shader_filename, GL_GEOMETRY_SHADER),)
        if comp_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(comp_shader_filename, GL_COMPUTE_SHADER),)
        if tess_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(tess_shader_filename, GL_TESS_CONTROL_SHADER),)
        if wtff_shader_filename != None: 
            shader_tuple += (ShaderLoader.compile_shader(wtff_shader_filename, GL_REFERENCED_BY_COMPUTE_SHADER),)

        shader = compileProgram(*shader_tuple)
        
        print(f"Shaders loaded: {shader}")
        return shader
    
if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")