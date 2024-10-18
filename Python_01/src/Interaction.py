

import glfw
from OpenGL.GL import *
import pyrr

import logging, os
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(),
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.DEBUG)

class ViewHandler():
    location = pyrr.Vector3([0.0, 1.0, 0.0])
    up_vec = pyrr.Vector3([0.0, 1.0, 0.0])
    fwd_vec = pyrr.Vector3([0.0, 0.0, -1.0])

    def move(new_location):
        pyrr.Vector3(new_location)        



class EHandler():
    window_dims = 800, 600

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
    model_data = [0.0, 0.0, 0.0]

    proj_vec =  pyrr.matrix44.create_perspective_projection_matrix(
        FOV, window_dims[0]/window_dims[1], NEAR, FAR)

    DONE = False
    MODELNUM = 0
    SHADERNUM = 0
    KEY = 0

    def __init__(self):
        self.log = logging.getLogger(__file__)        


    # @staticmethod
    def configure(self, window):
        glfw.set_window_size_callback(window, self.window_size_callback)
        self.window_size = glfw.get_window_size(window)
        # Set some other fun callbacks
        glfw.set_key_callback(window, self.key_callback)
        glfw.set_char_callback(window, self.char_callback)
        glfw.set_char_mods_callback(window, self.char_mods_callback)
        glfw.set_cursor_pos_callback(window, self.cursor_pos_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        glfw.set_joystick_callback(self.joystick_callback)   
        self.log.info(f"window_size={self.window_size}")

    # @staticmethod
    def window_size_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        self.window_dims = width, height
        self.proj_vec =  pyrr.matrix44.create_perspective_projection_matrix(self.FOV, width/height, self.NEAR, self.FAR)
        # glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.proj_mtx)
        self.log.info(f"window_size={self.window_size}")
    
    # @staticmethod
    def cursor_pos_callback(self, window, x, y):
        self.mouse_dxdy = (x - self.mouse_coords[0], y - self.mouse_coords[1])
        self.mouse_coords = x, y
        if self.mouse_buttons == 0 and self.mouse_down == 1:  # Is mouse button 0 down?
            # self.log.info(f"mouse_mov={self.mouse_dxdy} gimbal angles {self.model_axis[0]},{self.model_axis[1]},{self.model_axis[2]}")
            self.model_axis[0] -= self.mouse_dxdy[1] / 4.0
            self.model_axis[1] -= self.mouse_dxdy[0] / 4.0
        if self.mouse_buttons == 1 and self.mouse_down == 1:  # Is mouse button 0 down?
            # self.log.info(f"mouse_mov={self.mouse_dxdy} gimbal angles {self.model_axis[0]},{self.model_axis[1]},{self.model_axis[2]}")
            self.model_data[0] -= self.mouse_dxdy[1] / 4.0
            self.model_data[1] -= self.mouse_dxdy[0] / 4.0
    
    # @staticmethod
    def mouse_button_callback(self, window, a, b, c):
        self.log.info(f"mouse_button_callback button={a} down={b} c={c}")
        self.mouse_buttons = a
        self.mouse_down = b

    # @staticmethod
    def key_callback(self, window, a, b, c, d):
        self.log.info(f"key_callback a={a} b={b} c={c} d={d}")
        if a==256 and b == 9:
            self.DONE = True
        if b == 68:
            self.MODELNUM = 0
        if b == 69:
            self.MODELNUM = 1
        if b == 70:
            self.MODELNUM = 2
        if b == 71:
            self.SHADERNUM = 0
        if b == 72:
            self.SHADERNUM = 1
        if b == 73:
            self.SHADERNUM = 2
        # if b == 74:
        #     self.SHADERNUM = 3
        if b == 95:  # F11
            self.TOGGLESCREEN = 1


    # @staticmethod
    def char_callback(self, window, a):
        self.log.info(f"char_callback char={a}")

    # @staticmethod
    def char_mods_callback(self, window, a, b):
        self.log.info(f"char_mods_callback a={a} b={b}")

    def scroll_callback(self, window, a, b):
        self.log.info(f"scroll_callback a={a} b={b}")
        self.mouse_scroll = b
        self.DIST += b

    # @staticmethod
    def joystick_callback(self, window, arg):
        self.log.info(f"joystick_callback a={arg}")    

if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # self.log.info(model)
    from AnOpenGLprogram import ReviewOpenGL
    ReviewOpenGL.main()