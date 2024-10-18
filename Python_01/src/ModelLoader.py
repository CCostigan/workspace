

from OpenGL.GL import *

import numpy as np

from TextureLoader import TextureLoader

import logging, os
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(),
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.DEBUG)

# https://stackoverflow.com/questions/16380005/opengl-3-4-glvertexattribpointer-stride-and-offset-miscalculation

model_home = "res/mdls/"
image_home = "res/imgs/"

class ModelLoader():

    def __init__(self):
        self.log = logging.getLogger(__file__)    
        self.tl = TextureLoader()    
       
    def model_Elements(self, filename):
        objmod = self.load_model_obj(filename)    

    def model_Arrays(self, filename):
        objmod = self.load_model_obj(filename)

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


    def load_model_obj(self, filename):

        vtxs = [] # Vertex Coords
        norm = [] # Vertex Normals
        txuv = [] # Texture Coords
        face = [] # Face vertex lists
        mats = {} # Materials

        indx = [] # Index for buffer
        bufr = [] # Vertex Buffer
        
        with open(model_home+filename, 'r') as f:
            textures = []
            line = f.readline()
            while line:
                tokens = line.split()
                # self.log.info(f"Line={tokens[1:]}")  
                if len(tokens) == 0:  # Empty line
                    pass
                elif tokens[0] == '#':  # Comment line
                    pass
                elif tokens[0] == 'o':  # Object                    
                    pass
                elif tokens[0] == 'mtllib': # Material
                    mats.update(self.load_model_material(textures, tokens[1]))
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
                    self.log.info(f"Unknown objet token {tokens[0]}")
                line = f.readline()

            # self.log.info(f"vtxs count = {len(vtxs)}")
            # self.log.info(f"txuv count = {len(txuv)}")
            # self.log.info(f"norm count = {len(norm)}")
            # self.log.info(f"face count = {len(face)}")
            
            # self.log.info(f"indx len = {len(indx)}")
            ## self.log.info(f"indx={indx}")
            # self.log.info(f"bufr len = {len(bufr)}")
            ## self.log.info(f"bufr={bufr}")

            indxs = np.array(indx, np.int32)
            buffr = np.array(bufr, np.float32)

        return {
            "indxs" : indxs, 
            "buffr" : buffr,
            "textures": textures
        }


    def load_model_material(self, textures, filename):

        matlist = [] # Overall list of materials
        
        material = { # Set up the default material in case the mat file is junk
            "name":"Default",
            "map_Kd": self.tl.load_texture(image_home + "NO-IMAGE"),
            "ambient" : (1.0, 1.0, 1.0),
            "diffuse" : (1.0, 0.0, 0.0),
            "specular" : (0.0, 1.0, 0.0),
            "emission" : (0.0, 0.0, 1.0),
        } 

        # self.log.info(f"LOADING MATERIAL {filename}")        
        with open(model_home+filename, 'r') as f:
            line = f.readline()
            while line:
                tokens = line.split()
                if len(tokens) == 0:  # Empty line
                    pass
                elif tokens[0] == '#':  # Comment line
                    pass
                #  First legit line in the mats file is usually the 'New Material' line
                elif tokens[0] == 'newmtl':
                    material["newmtl"] = tokens[1]
                elif tokens[0] == 'map_Kd':  # Object    
                    textures.append(self.tl.load_texture(image_home + tokens[1]))
                elif tokens[0] == "illum":  # Illumination value?
                    material["illum"] = float(tokens[1])
                elif tokens[0] == "d":  # Transmission Color Tr = 1 - d
                    material["transmid"] = float(tokens[1])
                elif tokens[0] == 'Ns':  # One float
                    material["Ns"] = float(tokens[1])
                elif tokens[0] == 'Ni':  # 
                    material["Ni"] = float(tokens[1])
                elif tokens[0] == 'Ka':  # Ambient
                    material["ambient"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Kd':  # Diffuse
                    material["diffuse"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Ks':  # Specular
                    material["specular"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == 'Ke':  # 
                    material["emission"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "Tr":  # Transmission Color
                    material["transmit"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "Tf":  # Transmission Filter Color
                    material["filterc"] = (float(tokens[1]),float(tokens[2]),float(tokens[3]))
                elif tokens[0] == "map_Kd":  # Filename of Diffuse texture
                    self.log.info(f"+Diffuse {tokens[1]}")
                elif tokens[0] == "map_Ke":  # Filename of Emission texture
                    self.log.info(f"+Emission {tokens[1]}")
                elif tokens[0] == "map_Ks":  # Filename of Specular texture
                    self.log.info(f"+Specular {tokens[1]}")
                elif tokens[0] == "map_Ns":  # Filename of Specular highlight texture
                    self.log.info(f"+SpecularH {tokens[1]}")
                elif tokens[0] == "map_d":   # Filename of Alpha texture
                    self.log.info(f"+Alpha {tokens[1]}")
                elif tokens[0] == "map_bump":  # Filename of Bumpmap texture
                    self.log.info(f"+Bumpmap {tokens[1]}")
                elif tokens[0] == "bump":  # See above
                    self.log.info(f"+Bumpmap2 {tokens[1]}")
                elif tokens[0] == "disp":  # Filename of Displacement texture
                    self.log.info(f"+Displacement {tokens[1]}")
                elif tokens[0] == "decal":  # Filename of Stencil Decal texture
                    self.log.info(f"+StencilDecal {tokens[1]}")
                elif tokens[0] == "refl":  # Filename of Spherical Reflection texture
                    self.log.info(f"+SphericalReflect {tokens[1]}")
                else:
                    self.log.info(f"!!! Unrecognized token '{tokens[0]}' in {filename}")

                line = f.readline()
        return matlist        




if __name__=='__main__':
    # model = ModelLoader.load_model_obj("res/mdls/Cube.obj")
    # self.log.info(model)
    from AnOpenGLprogram import ReviewOpenGL
    rogl = ReviewOpenGL()
    rogl.main()
