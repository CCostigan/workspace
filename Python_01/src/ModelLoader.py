

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

        vtxs = [] # Vertex Coords
        norm = [] # Vertex Normals
        txuv = [] # Texture Coords
        face = [] # Face vertex lists

        indx = [] # Index for buffer
        bufr = [] # Vertex Buffer
        
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

        mtls = [] # Materials loader

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
                    mtls.append(tokens[1])
                elif tokens[0] == "illum":  # Illumination value?
                    illum = int(tokens[1])
                elif tokens[0] == 'Ns':  # One float
                    Ns = float(tokens[1])
                elif tokens[0] == 'Ni':  # 
                    Ni = float(tokens[1])
                elif tokens[0] == 'Ka':  # Ambient
                    ambient = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Kd':  # Diffuse
                    diffuse = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Ks':  # Specular
                    specular = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Ke':  # 
                    emission = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "Tr":  # Transmission Color
                    transmit = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "d":  # Transmission Color Tr = 1 - d
                    transmid = float(tokens[1])
                elif tokens[0] == "Tf":  # Transmission Filter Color
                    filterc = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "map_Kd":  # Filename of Diffuse texture
                    print(f"+Diffuse {tokens[1]}")
                elif tokens[0] == "map_Ke":  # Filename of Emission texture
                    print(f"+Emission {tokens[1]}")
                elif tokens[0] == "map_Ks":  # Filename of Specular texture
                    print(f"+Specular {tokens[1]}")
                elif tokens[0] == "map_Ns":  # Filename of Specular highlight texture
                    print(f"+SpecularH {tokens[1]}")
                elif tokens[0] == "map_d":   # Filename of Alpha texture
                    print(f"+Alpha {tokens[1]}")
                elif tokens[0] == "map_bump":  # Filename of Bumpmap texture
                    print(f"+Bumpmap {tokens[1]}")
                elif tokens[0] == "bump":  # See above
                    print(f"+Bumpmap2 {tokens[1]}")
                elif tokens[0] == "disp":  # Filename of Displacement texture
                    print(f"+Displacement {tokens[1]}")
                elif tokens[0] == "decal":  # Filename of Stencil Decal texture
                    print(f"+StencilDecal {tokens[1]}")
                elif tokens[0] == "refl":  # Filename of Spherical Reflection texture
                    print(f"+SphericalReflect {tokens[1]}")
                else:
                    print(f"!!! Unrecognized token '{tokens[0]}' in {filename}")

                line = f.readline()
        pass




if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # print(model)
    from AnOpenGLprogram import ReviewOpenGL
    ReviewOpenGL.main()
