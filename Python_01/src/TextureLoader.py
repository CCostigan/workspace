
from OpenGL.GL import *
from PIL import Image
import os 

import logging 
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(),
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname).3s %(filename)s:%(lineno)-4s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.DEBUG)

class TextureLoader():

    def __init__(self):
        self.log = logging.getLogger(__file__)        

    # @staticmethod
    def load_texture(self, filename): 

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # load image
        data = bytes.fromhex(" 02 07 fa ff fc f8 07 ff fe 01 01 ff 04 fb 04 ff")
        width = height = 2
        if os.path.exists(filename):
            # self.log.info(f"Loading texture {filename}")
            image = Image.open(filename)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            data = image.convert("RGBA").tobytes()
            width = image.width
            height = image.height
            self.log.info(f"Texture Loader load: {filename} len={len(data)}")
            # self.log.info(f"Using default texture {data}")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        # self.log.info(f"Loaded texture {filename}")
        return texture


