
import numpy as np
from OpenGL.GL import *
from TextureLoader import TextureLoader
import random
import pyrr

class Writer():

    def __init__(self, workarea):
        self.charstrip = TextureLoader.load_texture("res/imgs/charstrip.png")

        self.count = 0
        indx = []
        bufr = []

        for i in range (0, 256):
            y1 = 1/256 * i
            y2 = 1/256 * (i+1)

            indx.append(len(bufr))
            bufr.extend([0.0, 0.0, 0.0])
            bufr.extend([0.0, y1])
            bufr.extend([0.0, 0.0, 1.0])

            indx.append(len(bufr))
            bufr.extend([1.0, 0.0, 0.0])
            bufr.extend([1.0, y1])
            bufr.extend([0.0, 0.0, 1.0])

            indx.append(len(bufr))
            bufr.extend([1.0, 1.0, 0.0])
            bufr.extend([1.0, y2])
            bufr.extend([0.0, 0.0, 1.0])

            indx.append(len(bufr))
            bufr.extend([0.0, 1.0, 0.0])
            bufr.extend([0.0, y2])
            bufr.extend([0.0, 0.0, 1.0])
            pass

        self.indxs = np.array(indx, np.int32)
        self.buffr = np.array(bufr, np.float32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.buffr.nbytes, self.buffr, GL_STATIC_DRAW)
        # Vertex coords
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.buffr.itemsize * 8, ctypes.c_void_p(0))
        # UV coords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.buffr.itemsize * 8, ctypes.c_void_p(12))
        # Normal vectors
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.buffr.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2) 

        self.m_ortho = pyrr.matrix44.create_orthogonal_projection_matrix(workarea[0], workarea[2], workarea[3], workarea[1], -1.0, 1.0)


    def draw(self, display_string):
        glBindVertexArray(self.VAO)
        glBindTexture(GL_TEXTURE_2D, self.charstrip)
        for asciicode in bytearray(display_string, 'ascii'):
            glDrawArrays(GL_QUADS, asciicode, asciicode+1)
            pass





