
from OpenGL.GL import *
from PIL import Image
import os 
class TextureLoader():

    def load_texture(filename): 

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
            print(f"Loading texture {filename}")
            image = Image.open(filename)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            data = image.convert("RGBA").tobytes()
            width = image.width
            height = image.height
            print(f"Texture Loader load: {filename} len={len(data)}")
            print(data)
        else:
            print(f"Using default texture {data}")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        print(f"Loaded texture {filename}")
        return texture


