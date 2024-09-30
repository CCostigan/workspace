#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr

from TextureLoader import TextureLoader
from ShaderLoader import ShaderLoader
from ModelLoader import ModelLoader
from Interaction import EHandler


WIDTH, HEIGHT = 1600, 900
MIN, MAX = 0.1, 10000.0
model_axis = [0.0, 0.0, 0.0]

class ReviewOpenGL(object):

    def main():

        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # glfw.window_hint(glfw.SAMPLES, 1)

        # creating the window
        window = glfw.create_window(WIDTH, HEIGHT, "Python OpenGL window", None, None)
        # check if window was created
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        
        # fb_size = glfw.get_framebuffer_size(window)
        glfw.set_window_pos(window, 10, 30)
        glfw.make_context_current(window)

        eh = EHandler.configure(window)

        shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")

        ml = ModelLoader()
        models = [
            # ml.model_Elements_HC(),
            # ml.model_Elements("res/mdls/Cube.obj"),
            ml.model_Arrays("res/mdls/DDG.obj"),
        ]
        for model in models:
            print(model)

        charstrip = TextureLoader.load_texture("res/imgs/charstrip.png")
        # picture = TextureLoader.load_texture("res/imgs/pic2.png")
        picture = TextureLoader.load_texture("res/imgs/ddg0.png")
        person = TextureLoader.load_texture("res/imgs/lena.jpg")

        glUseProgram(shader)
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Initial Viewport
        glViewport(0, 0, WIDTH, HEIGHT)

        # Matrices for the view to be fed to the shaders
        # proj_vec = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH/HEIGHT, 0.1, 10000.0)
        # tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -EHandler.DIST]))

        # Talk to the shaders
        uniform_modl = glGetUniformLocation(shader, "model")
        uniform_proj = glGetUniformLocation(shader, "proj")

        # the main application loop
        while not glfw.window_should_close(window) and not EHandler.DONE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -EHandler.DIST]))

            glfwtime = glfw.get_time()
            rot_x = pyrr.Matrix44.from_x_rotation(0.01 * EHandler.model_axis[0]) #0.0 * glfwtime)
            rot_y = pyrr.Matrix44.from_y_rotation(0.01 * EHandler.model_axis[1]) #0.8 * glfwtime)
            # rot_z = pyrr.Matrix44.from_z_rotation(0.01 * EHandler.model_axis[2]) #0.8 * glfwtime)
            rotation_mtx = pyrr.matrix44.multiply(rot_y, rot_x)
            # rotation_mtx = pyrr.matrix44.multiply(rotation_mtx, rot_z)
            model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)
            glUniformMatrix4fv(uniform_modl, 1, GL_FALSE, model_mtx)
            glUniformMatrix4fv(uniform_proj, 1, GL_FALSE, EHandler.proj_vec)
            for model in models:
                if model["render"] == "DrawElements":
                    glBindTexture(GL_TEXTURE_2D, person)
                    glDrawElements(GL_TRIANGLES, len(model["indx"]), GL_UNSIGNED_INT, None)
                if model["render"] == "DrawArrays":
                    glBindTexture(GL_TEXTURE_2D, picture)
                    glDrawArrays(GL_TRIANGLES, 0, len(model["indx"]))


            glfw.swap_buffers(window)
        glfw.terminate()


if __name__=='__main__':
    ReviewOpenGL.main()



