#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr


WIDTH, HEIGHT = 1600, 900
MIN, MAX = 0.1, 10000.0

class ReviewOpenGL(object):
    DONE = False

    def window_size_callback(window, width, height):
        print(f"Width={width} Height={height}")
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, MIN, MAX)
        # glUniformMatrix4fv(ReviewOpenGL.proj_loc, 1, GL_FALSE, ReviewOpenGL.proj_mtx)
        pass
    
    @staticmethod
    def cursor_pos_callback(window, x, y):
        if False:  # Need to log fewer of these
            print(f"x={x} y={y}")
        pass
    def mouse_button_callback(window, a, b, c):
        print(f"mouse_button_callback button={a} down={b} c={c}")

    def key_callback(window, a, b, c, d):
        print(f"key_callback a={a} b={b} c={c} d={d}")
        if a==256 and b == 9:
            ReviewOpenGL.DONE = True

    def char_callback(window, a):
        print(f"char_callback char={a}")

    def char_mods_callback(window, a, b):
        print(f"char_mods_callback a={a} b={b}")

    def joystick_callback(window, arg):
        print(f"joystick_callback a={arg}")

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
        glfw.set_window_size_callback(window, ReviewOpenGL.window_size_callback)
        # Set some other fun callbacks
        glfw.set_key_callback(window, ReviewOpenGL.key_callback)
        glfw.set_char_callback(window, ReviewOpenGL.char_callback)
        glfw.set_char_mods_callback(window, ReviewOpenGL.char_mods_callback)
        glfw.set_cursor_pos_callback(window, ReviewOpenGL.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, ReviewOpenGL.mouse_button_callback)
        glfw.set_joystick_callback(ReviewOpenGL.joystick_callback)

        from ShaderLoader import ShaderLoader
        shader = ShaderLoader.load_shader("shader_vert.glsl","shader_frag.glsl")

        from ModelLoader import ModelLoader
        model = ModelLoader.load_model("res/mdls/Cube.obj")

        from TextureLoader import TextureLoader
        texture = TextureLoader.load_texture("res/imgs/texture.png")

        glUseProgram(shader)
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        up_vec = pyrr.Vector3([0.0, 1.0, 0.0])
        home_vec = pyrr.Vector3([10.0, 0.0, 0.0])
        model_vec = pyrr.Vector3([0.0, 0.0, 0.0])
        # Matrices for the view to be fed to the shaders
        glViewport(0, 0, WIDTH, HEIGHT)
        proj_mtx = pyrr.matrix44.create_perspective_projection_matrix(85, WIDTH / HEIGHT, MIN, MAX)
        model_pos = pyrr.matrix44.create_from_translation(model_vec)
        view_mtx = pyrr.matrix44.create_look_at(home_vec, model_vec, up_vec)

        # Talk to the shaders
        modl_loc = glGetUniformLocation(shader, "model")
        proj_loc = glGetUniformLocation(shader, "proj")
        view_loc = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, proj_mtx)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view_mtx)

        # the main application loop
        while not glfw.window_should_close(window) and not ReviewOpenGL.DONE:
            glfw.poll_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if True:
                rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
                model_mtx = pyrr.matrix44.multiply(rot_y, model_pos)

                glBindVertexArray(model["vao"][0])
                glBindTexture(GL_TEXTURE_2D, texture)
                glUniformMatrix4fv(modl_loc, 1, GL_FALSE, model_mtx)
                glDrawArrays(GL_TRIANGLES, 0, len(model["indx"]))


            glfw.swap_buffers(window)

        glfw.terminate()


if __name__=='__main__':
    ReviewOpenGL.main()



