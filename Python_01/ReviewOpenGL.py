#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr

from Interaction import *

WIDTH, HEIGHT = 1600, 900
MIN, MAX = 0.1, 10000.0

class ReviewOpenGL(object):

    def main():

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
        
        # fb_size = glfw.get_framebuffer_size(window)
        glfw.set_window_pos(window, 10, 30)

        glfw.make_context_current(window)

        eh = EHandler.configure(window)

        use_hc_model = True

        from ShaderLoader import ShaderLoader
        shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")

        from ModelLoader import ModelLoader
        if use_hc_model == True:
            model = ModelLoader.null_model()
        else:
            model = ModelLoader.load_model("res/mdls/Cube.obj")

        from TextureLoader import TextureLoader
        texture = TextureLoader.load_texture("res/imgs/texture.png")

        glUseProgram(shader)
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # up_vec = pyrr.Vector3([0.0, 1.0, 0.0])
        # home_vec = pyrr.Vector3([0.0, 4.0, 3.0])
        # nose_vec = pyrr.Vector3([0.0, 0.0, -1.0])
        # model_vec = pyrr.Vector3([0.0, 0.0, 0.0])
        # Matrices for the view to be fed to the shaders
        glViewport(0, 0, WIDTH, HEIGHT)
        # proj_mtx = pyrr.matrix44.create_perspective_projection_matrix(85, WIDTH / HEIGHT, MIN, MAX)
        # model_pos = pyrr.matrix44.create_from_translation(model_vec)
        # view_mtx = pyrr.matrix44.create_look_at(home_vec, home_vec+nose_vec, up_vec)
        proj_vec = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH/HEIGHT, 0.1, 100)
        tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -30]))

        # Talk to the shaders
        uniform_modl = glGetUniformLocation(shader, "model")
        # Will set this in the main loop
        uniform_proj = glGetUniformLocation(shader, "proj")
        # glUniformMatrix4fv(proj_loc, 1, GL_FALSE, proj_mtx)
        # view_loc = glGetUniformLocation(shader, "view")
        # glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_mtx)
        glUniformMatrix4fv(uniform_proj, 1, GL_FALSE, proj_vec)

        # the main application loop
        while not glfw.window_should_close(window) and not EHandler.DONE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


            if use_hc_model:
                glfwtime = glfw.get_time()
                rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfwtime)
                rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwtime)
                rotation_mtx = pyrr.matrix44.multiply(rot_x, rot_y)
                model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)
                glUniformMatrix4fv(uniform_modl, 1, GL_FALSE, model_mtx)
                glDrawElements(GL_TRIANGLES, len(model["indx"]), GL_UNSIGNED_INT, None)

            # elif model["indx"] is not None:
            #     rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
            #     rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
            #     rotation_mtx = pyrr.matrix44.multiply(rot_x, rot_y)
            #     model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)
            #     glUniformMatrix4fv(uniform_modl, 1, GL_FALSE, model_mtx)
                # glDrawArrays(GL_TRIANGLES, 0, len(model["indx"]))


            glfw.swap_buffers(window)
        glfw.terminate()


if __name__=='__main__':
    ReviewOpenGL.main()



