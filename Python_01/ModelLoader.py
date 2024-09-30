

from OpenGL.GL import *

import numpy as np

from TextureLoader import TextureLoader


# https://stackoverflow.com/questions/16380005/opengl-3-4-glvertexattribpointer-stride-and-offset-miscalculation

class ModelLoader():

    # def __init__(self, mode=0, filename=None):
    #     elif mode == 1:
    #         self.result = self.model_Elements_HC()
    #     elif mode == 2 and filename is not None:
    #         self.result = self.model_Elements(filename)
    #     elif mode == 3 and filename is not None:
    #         self.result = self.model_Arrays(filename)
        
    def model_Elements_HC(self):
        vertices = [-0.5, -0.5,  0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                     0.5, -0.5,  0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                     0.5,  0.5,  0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                    -0.5,  0.5,  0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
   
                    -0.5, -0.5, -0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                     0.5, -0.5, -0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                     0.5,  0.5, -0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                    -0.5,  0.5, -0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
   
                     0.5, -0.5, -0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                     0.5,  0.5, -0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                     0.5,  0.5,  0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                     0.5, -0.5,  0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
   
                    -0.5,  0.5, -0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                    -0.5, -0.5, -0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                    -0.5, -0.5,  0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                    -0.5,  0.5,  0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
   
                    -0.5, -0.5, -0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                     0.5, -0.5, -0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                     0.5, -0.5,  0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                    -0.5, -0.5,  0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
   
                     0.5,  0.5, -0.5,    0.0, 0.0,    0.0, 0.0, 1.0,
                    -0.5,  0.5, -0.5,    1.0, 0.0,    0.0, 0.0, 1.0,
                    -0.5,  0.5,  0.5,    1.0, 1.0,    0.0, 0.0, 1.0,
                     0.5,  0.5,  0.5,    0.0, 1.0,    0.0, 0.0, 1.0,
        ]

        indices = [ 0,  1,  2,  2,  3,  0,
                    4,  5,  6,  6,  7,  4,
                    8,  9, 10, 10, 11,  8,
                    12, 13, 14, 14, 15, 12,
                    16, 17, 18, 18, 19, 16,
                    20, 21, 22, 22, 23, 20
        ]
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)
        # Vertex Buffer Object
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(12))        
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 8, ctypes.c_void_p(20))        
        glEnableVertexAttribArray(2)

        print("Default model loaded")
        return {
            "render" : "DrawElements",
            "vao" : None,
            "vbo" : VBO,
            "ebo" : EBO,
            "indx" : indices, 
            "bufr" : vertices, 
            "textures" : [], 
        }

    def model_Elements(self, filename):
        objmod = ModelLoader.load_model_obj(filename)
        # VBO = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # glBufferData(GL_ARRAY_BUFFER, objmod["buffr"].nbytes, objmod["buffr"], GL_STATIC_DRAW)

        # # Element Buffer Object
        # EBO = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, objmod["indxs"].nbytes, objmod["indxs"], GL_STATIC_DRAW)

        # glEnableVertexAttribArray(0)
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(0))

        # glEnableVertexAttribArray(1)
        # glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(12))

        # glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(20))
        # glEnableVertexAttribArray(2)

        # print("Default model loaded")
        # return {
        #     "render" : "DrawElements",
        #     "vao" : None,
        #     "vbo" : VBO,
        #     "ebo" : EBO,
        #     "indx" : objmod["indxs"], 
        #     "bufr" : objmod["buffr"], 
        #     "textures" : objmod["textures"], 
        # }
    

    def model_Arrays(self, filename):
        objmod = ModelLoader.load_model_obj(filename)

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, objmod["buffr"].nbytes, objmod["buffr"], GL_STATIC_DRAW)

        # Vertex coords
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(0))
        # UV coords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(12))
        # Normal vectors
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, objmod["buffr"].itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2) 

        return {
            "render" : "DrawArrays",
            "vao" : VAO, 
            "vbo" : VBO,
            "ebo" : None,
            "indx" : objmod["indxs"], 
            "bufr" : objmod["buffr"], 
            "textures" : objmod["textures"], 
        }


    def load_model_obj(filename):

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
                elif tokens[0] == 'o':  # Object                    
                    pass
                elif tokens[0] == 'mtllib': # Material
                    pass
                elif tokens[0] == 'usemtl': # Set Current
                    pass
                elif tokens[0] == 's': # ?
                    pass
                elif tokens[0] == 'v': # Vertex
                    for tokn in tokens[1:]:
                        vtxs.append(float(tokn))
                elif tokens[0] == 'vt': # Texture
                    for tokn in tokens[1:]:
                        txuv.append(float(tokn))
                elif tokens[0] == 'vn': # Normal
                    for tokn in tokens[1:]:
                        norm.append(float(tokn))
                elif tokens[0] == 'f': # Face
                    # face.append(tokens)
                    for tokn in tokens[1:]:
                        tkns = tokn.split('/')
                        indx.append(len(bufr))
                        # print(tkns)
                        # indx.append(int(tkns[0])-1)
                        # indx.append(len(bufr))
                        v = (int(tkns[0])-1) * 3
                        t = (int(tkns[1])-1) * 2
                        n = (int(tkns[2])-1) * 3
                        bufr.extend(vtxs[v:v+3])
                        bufr.extend(txuv[t:t+2])
                        bufr.extend(norm[n:n+3])
                else:
                    print(f"Unknown objet token {tokens[0]}")
                line = f.readline()

            print(f"vtxs count = {len(vtxs)}")
            print(f"txuv count = {len(txuv)}")
            print(f"norm count = {len(norm)}")
            print(f"face count = {len(face)}")
            
            print(f"indx len = {len(indx)}")
            # print(f"indx={indx}")
            print(f"bufr len = {len(bufr)}")
            # print(f"bufr={bufr}")

            indxs = np.array(indx, np.int32)
            buffr = np.array(bufr, np.float32)

        texture = TextureLoader.load_texture("res/imgs/lena.jpg")
        glBindTexture(GL_TEXTURE_2D, texture)

        return {
            "indxs" : indxs, 
            "buffr" : buffr,
            "textures": [texture]
        }


if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # print(model)
    from ReviewOpenGL import ReviewOpenGL
    ReviewOpenGL.main()
