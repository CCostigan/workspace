

from OpenGL.GL import *
from OpenGL.GL.shaders import *  #compileProgram, compileShader


class ShaderLoader():

    def load_shader_hc():

        vertex_src = """
        # version 330

        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec2 a_texture;

        uniform mat4 model; // combined translation and rotation
        uniform mat4 proj;

        out vec3 v_color;
        out vec2 v_texture;

        void main()
        {
            gl_Position = proj * model * vec4(a_position, 1.0);
            v_texture = a_texture;
        }
        """

        fragment_src = """
        # version 330

        in vec2 v_texture;

        out vec4 out_color;

        uniform sampler2D s_texture;

        void main()
        {
            out_color = texture(s_texture, v_texture);
        }
        """
        vert_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
        frag_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)    

        shader = compileProgram(vert_shader,frag_shader)

        print(f"Shaders loaded: {shader}")
        return shader

    def load_shader(
            vertex_shader_filename, 
            fragment_shader_filename  ):

        shader_home="res/shaders/"

        with open(shader_home+vertex_shader_filename, 'r') as vertex_file:
            vertex_shader_src = vertex_file.readlines()
        vert_shader = compileShader(vertex_shader_src, GL_VERTEX_SHADER)


        with open(shader_home+fragment_shader_filename, 'r') as fragment_file:
            fragment_shader_src = fragment_file.readlines()
        frag_shader = compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)    

        shader = compileProgram(vert_shader,frag_shader)
        # glReleaseShaderCompiler()  # GL4

        print(f"Shaders loaded: {shader}")
        return shader
    
if __name__=='__main__':
    shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")
    print(f"Shader loader={shader}")