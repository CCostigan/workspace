

import glfw
from OpenGL.GL import *
import pyrr

class EHandler():
    dims = 800, 600

    mouse_buttons = 0
    mouse_down = 0
    mouse_coords = 400, 300
    mouse_dxdy = 0, 0

    NEAR = 0.1
    FAR = 10000.0
    DONE = False

    def __init__():
        pass

    def configure(window):

        glfw.set_window_size_callback(window, EHandler.window_size_callback)
        EHandler.window_size = glfw.get_window_size(window)
        # Set some other fun callbacks
        glfw.set_key_callback(window, EHandler.key_callback)
        glfw.set_char_callback(window, EHandler.char_callback)
        glfw.set_char_mods_callback(window, EHandler.char_mods_callback)
        glfw.set_cursor_pos_callback(window, EHandler.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, EHandler.mouse_button_callback)
        glfw.set_joystick_callback(EHandler.joystick_callback)   
        print(f"window_size={EHandler.window_size}")

    # @staticmethod
    def window_size_callback(window, width, height):
        glViewport(0, 0, width, height)
        EHandler.dims = width, height
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, EHandler.NEAR, EHandler.FAR)
        # glUniformMatrix4fv(ReviewOpenGL.proj_loc, 1, GL_FALSE, ReviewOpenGL.proj_mtx)
        print(f"window_size={EHandler.window_size}")
    
    # @staticmethod
    def cursor_pos_callback(window, x, y):
        EHandler.mouse_dxdy = (x - EHandler.mouse_coords[0], y - EHandler.mouse_coords[1])
        EHandler.mouse_coords = x, y
        if EHandler.mouse_buttons == 0 and EHandler.mouse_down == 1:  # Need to log fewer of these
            print(f"mouse_pos={EHandler.mouse_dxdy}")
    
    # @staticmethod
    def mouse_button_callback(window, a, b, c):
        print(f"mouse_button_callback button={a} down={b} c={c}")
        EHandler.mouse_buttons = a
        EHandler.mouse_down = b

    # @staticmethod
    def key_callback(window, a, b, c, d):
        print(f"key_callback a={a} b={b} c={c} d={d}")
        if a==256 and b == 9:
            EHandler.DONE = True

    # @staticmethod
    def char_callback(window, a):
        print(f"char_callback char={a}")

    # @staticmethod
    def char_mods_callback(window, a, b):
        print(f"char_mods_callback a={a} b={b}")

    # @staticmethod
    def joystick_callback(window, arg):
        print(f"joystick_callback a={arg}")    

