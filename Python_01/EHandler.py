

import glfw
from OpenGL.GL import *
import pyrr

class EHandler():
    mouse = 800, 600
    mdxdy = 0, 0
    DONE = False

    def __init__():
        pass

    def configure(window):

        glfw.set_window_size_callback(window, EHandler.window_size_callback)
        # Set some other fun callbacks
        glfw.set_key_callback(window, EHandler.key_callback)
        glfw.set_char_callback(window, EHandler.char_callback)
        glfw.set_char_mods_callback(window, EHandler.char_mods_callback)
        glfw.set_cursor_pos_callback(window, EHandler.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, EHandler.mouse_button_callback)
        glfw.set_joystick_callback(EHandler.joystick_callback)   
        mouse = glfw.get_window_size(window)
        print(f"Mouse={mouse}")

    def window_size_callback(window, width, height):
        print(f"Width={width} Height={height}")
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, MIN, MAX)
        # glUniformMatrix4fv(ReviewOpenGL.proj_loc, 1, GL_FALSE, ReviewOpenGL.proj_mtx)
        pass
    
    # @staticmethod
    def cursor_pos_callback(window, x, y):
        EHandler.mdxdy = (x - EHandler.mouse[0], y - EHandler.mouse[1])
        EHandler.mouse = x, y
        if True:  # Need to log fewer of these
            print(f"mouse={EHandler.mdxdy}")
    
    def mouse_button_callback(window, a, b, c):
        print(f"mouse_button_callback button={a} down={b} c={c}")

    def key_callback(window, a, b, c, d):
        print(f"key_callback a={a} b={b} c={c} d={d}")
        if a==256 and b == 9:
            EHandler.DONE = True

    def char_callback(window, a):
        print(f"char_callback char={a}")

    def char_mods_callback(window, a, b):
        print(f"char_mods_callback a={a} b={b}")

    def joystick_callback(window, arg):
        print(f"joystick_callback a={arg}")    