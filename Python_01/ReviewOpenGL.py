#!~/.venv/bin/python


import glfw
from OpenGL.GL import *


WIDTH, HEIGHT = 1600, 900

class ReviewOpenGL(object):

    def __init__(self):
        pass

    def window_size_callback():
        pass

    def main(self):
        pass

        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # # 4 MSAA is a good default with wide support
        glfw.window_hint(glfw.SAMPLES, 4)

        # creating the window
        window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)
        # check if window was created
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        
        # Query the actual framebuffer size so we can set the right viewport later
        # -> glViewport(0, 0, framebuffer_size[0], framebuffer_size[1])
        framebuffer_size = glfw.get_framebuffer_size(window)
        glfw.set_window_pos(window, 10, 30)

        glfw.make_context_current(window)
        # glfw.set_window_size_callback(window, self.window_size_callback)

        from ShaderLoader import ShaderLoader
        shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")

        from ModelLoader import ModelLoader
        model = ModelLoader.load_model("res/mdls/Cube.obj")

        from TextureLoader import TextureLoader
        texture = TextureLoader.load_texture("res/imgs/pic2.png")



        # the main application loop
        while not glfw.window_should_close(window):
            glfw.poll_events()




            glfw.swap_buffers(window)

        glfw.terminate()


if __name__=='__main__':
    rgl = ReviewOpenGL()
    rgl.main()
    pass



