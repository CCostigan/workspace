

import glfw
from OpenGL.GL import *
import pyrr

class ViewHandler():
    location = pyrr.Vector3([0.0, 1.0, 0.0])
    up_vec = pyrr.Vector3([0.0, 1.0, 0.0])
    fwd_vec = pyrr.Vector3([0.0, 0.0, -1.0])

    def move(new_location):
        pyrr.Vector3(new_location)        



class EHandler():
    window_dims = 1600, 900

    mouse_buttons = 0
    mouse_down = 0
    mouse_coords = 400, 300
    mouse_dxdy = 0, 0
    mouse_scroll = 0

    NEAR = 0.1
    FAR = 10000.0
    FOV = 30.0
    DIST = 30.0
    model_axis = [-25.0, -238.0, 0.0]

    proj_vec =  pyrr.matrix44.create_perspective_projection_matrix(
        FOV, window_dims[0]/window_dims[1], NEAR, FAR)

    DONE = False
    MODELNUM = 0
    SHADERNUM = 0

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
        glfw.set_scroll_callback(window, EHandler.scroll_callback)
        glfw.set_joystick_callback(EHandler.joystick_callback)   
        print(f"window_size={EHandler.window_size}")

    # @staticmethod
    def window_size_callback(window, width, height):
        glViewport(0, 0, width, height)
        EHandler.window_dims = width, height
        EHandler.proj_vec =  pyrr.matrix44.create_perspective_projection_matrix(EHandler.FOV, width/height, EHandler.NEAR, EHandler.FAR)
        # glUniformMatrix4fv(EHandler.proj_loc, 1, GL_FALSE, EHandler.proj_mtx)
        print(f"window_size={EHandler.window_size}")
    
    # @staticmethod
    def cursor_pos_callback(window, x, y):
        EHandler.mouse_dxdy = (x - EHandler.mouse_coords[0], y - EHandler.mouse_coords[1])
        EHandler.mouse_coords = x, y
        if EHandler.mouse_buttons == 0 and EHandler.mouse_down == 1:  # Is mouse button 0 down?
            # print(f"mouse_mov={EHandler.mouse_dxdy} gimbal angles {EHandler.model_axis[0]},{EHandler.model_axis[1]},{EHandler.model_axis[2]}")
            EHandler.model_axis[0] -= EHandler.mouse_dxdy[1] / 4.0
            EHandler.model_axis[1] -= EHandler.mouse_dxdy[0] / 4.0
    
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
        if b == 68:
            EHandler.MODELNUM = 0
        if b == 69:
            EHandler.MODELNUM = 1
        if b == 70:
            EHandler.MODELNUM = 2
        if b == 71:
            EHandler.SHADERNUM = 0
        if b == 72:
            EHandler.SHADERNUM = 1
        if b == 73:
            EHandler.SHADERNUM = 2
        # if b == 74:
        #     EHandler.SHADERNUM = 3

    # @staticmethod
    def char_callback(window, a):
        print(f"char_callback char={a}")

    # @staticmethod
    def char_mods_callback(window, a, b):
        print(f"char_mods_callback a={a} b={b}")

    def scroll_callback(window, a, b):
        # print(f"scroll_callback a={a} b={b}")
        EHandler.mouse_scroll = b
        EHandler.DIST += b

    # @staticmethod
    def joystick_callback(window, arg):
        print(f"joystick_callback a={arg}")    

if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # print(model)
    from ReviewOpenGL import ReviewOpenGL
    ReviewOpenGL.main()