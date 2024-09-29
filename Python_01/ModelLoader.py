

from OpenGL.GL import *

import numpy as np


class ModelLoader():


    def load_model(filename):

        vtxs = []
        norm = []
        txuv = []
        face = []

        indx = []
        bufr = []
        
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                tokens = line.split()
                # print(f"Line={tokens[1:]}")  
                if tokens[0] == '#':  # Comment line
                    pass
                if tokens[0] == 'o':  # Object                    
                    pass
                if tokens[0] == 'mtllib': # Material
                    pass
                if tokens[0] == 'usemtl': # Set Current
                    pass
                if tokens[0] == 's': # ?
                    pass
                if tokens[0] == 'v': # Vertex
                    for tokn in tokens[1:]:
                        vtxs.append(float(tokn))
                if tokens[0] == 'vt': # Texture
                    for tokn in tokens[1:]:
                        txuv.append(float(tokn))
                if tokens[0] == 'vn': # Normal
                    for tokn in tokens[1:]:
                        norm.append(float(tokn))
                if tokens[0] == 'f': # Face
                    for tokn in tokens[1:]:
                        tkns = tokn.split('/')
                        # print(tkns)
                        indx.append(int(tkns[0])-1)
                        v = (int(tkns[0])-1) * 3
                        t = (int(tkns[1])-1) * 2
                        n = (int(tkns[2])-1) * 3
                        bufr.extend(vtxs[v:v+3])
                        bufr.extend(txuv[t:t+2])
                        bufr.extend(norm[n:n+3])
                line = f.readline()

            print(f"vtxs count = {len(vtxs)}")
            print(f"txuv count = {len(txuv)}")
            print(f"norm count = {len(norm)}")
            print(f"face count = {len(face)}")
            
            print(f"indx len = {len(indx)}") # print(f"indx={indx}")
            print(f"bufr len = {len(bufr)}") # print(f"bufr={bufr}")

            indxs = np.array(indx, np.int32)
            buffr = np.array(vtxs, np.float32)

            VAO = glGenVertexArrays(2)
            VBO = glGenBuffers(2)

            glBindVertexArray(VAO[0])
            glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
            glBufferData(GL_ARRAY_BUFFER, buffr.nbytes, buffr, GL_STATIC_DRAW)

            # Vertex coords
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, buffr.itemsize * 8, ctypes.c_void_p(0))
            # UV coords
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, buffr.itemsize * 8, ctypes.c_void_p(12))
            # Normal vectors
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, buffr.itemsize * 8, ctypes.c_void_p(20))
            glEnableVertexAttribArray(2) 

        # return [indxs, buffr, VAO, VBO]
        return {
            "indx" : indxs, 
            "bufr" : buffr, 
            "vao" : VAO, 
            "vbo" : VBO
        }


if __name__ == '__main__':
    model = ModelLoader.load_model("res/mdls/Cube.obj")
    print(model)