

from OpenGL.GL import *

import numpy as np

from TextureLoader import TextureLoader


# https://stackoverflow.com/questions/16380005/opengl-3-4-glvertexattribpointer-stride-and-offset-miscalculation

model_home = "res/mdls/"
image_home = "res/imgs/"

class ModelLoader():

       
    def model_Elements(self, filename):
        objmod = ModelLoader.load_model_obj(filename)    

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
        
        with open(model_home+filename, 'r') as f:
            textures = []
            line = f.readline()
            while line:
                tokens = line.split()
                # print(f"Line={tokens[1:]}")  
                if len(tokens) == 0:  # Empty line
                    pass
                elif tokens[0] == '#':  # Comment line
                    pass
                elif tokens[0] == 'o':  # Object                    
                    pass
                elif tokens[0] == 'mtllib': # Material
                    ModelLoader.load_model_material(textures, tokens[1])
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
                    for i in range(2, len(tokens)-1):
                        
                        tkns = tokens[1].split('/')
                        indx.append(len(bufr))
                        v = (int(tkns[0])-1) * 3
                        t = (int(tkns[1])-1) * 2
                        n = (int(tkns[2])-1) * 3
                        bufr.extend(vtxs[v:v+3])
                        bufr.extend(txuv[t:t+2])
                        bufr.extend(norm[n:n+3])

                        tkns = tokens[i].split('/')
                        indx.append(len(bufr))
                        v = (int(tkns[0])-1) * 3
                        t = (int(tkns[1])-1) * 2
                        n = (int(tkns[2])-1) * 3
                        bufr.extend(vtxs[v:v+3])
                        bufr.extend(txuv[t:t+2])
                        bufr.extend(norm[n:n+3])
                        
                        tkns = tokens[i+1].split('/')
                        indx.append(len(bufr))
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

        return {
            "indxs" : indxs, 
            "buffr" : buffr,
            "textures": textures
        }


    def load_model_material(textures, filename):
        print(f"LOADING MATERIAL {filename}")        
        with open(model_home+filename, 'r') as f:
            line = f.readline()
            while line:
                tokens = line.split()
                if len(tokens) == 0:  # Empty line
                    pass
                elif tokens[0] == '#':  # Comment line
                    pass
                elif tokens[0] == 'map_Kd':  # Object    
                    print(f"Texture {tokens[1]}")
                    textures.append(TextureLoader.load_texture(image_home + tokens[1]))
                    pass
                elif tokens[0] == 'newmtl':
                    pass
                elif tokens[0] == 'Ns':
                    pass
                elif tokens[0] == 'Ka':
                    pass
                elif tokens[0] == 'Kd':
                    pass
                elif tokens[0] == 'Ks':
                    pass
                elif tokens[0] == 'Ke':
                    pass
                elif tokens[0] == 'Ni':
                    pass
                elif tokens[0] == 'd':
                    pass
                elif tokens[0] == 'illum':
                    pass

                else:
                    print(f"Unrecognized token '{tokens[0]}' in {filename}")

                line = f.readline()
        pass




if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # print(model)
    from AnOpenGLprogram import ReviewOpenGL
    ReviewOpenGL.main()
