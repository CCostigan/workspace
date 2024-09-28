
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
                        print(tkns)
                        indx.append(int(tkns[0])-1)
                        v = (int(tkns[0])-1) * 3
                        t = (int(tkns[1])-1) * 2
                        n = (int(tkns[2])-1) * 3
                        bufr.extend(vtxs[v:v+3])
                        bufr.extend(txuv[t:t+2])
                        bufr.extend(norm[n:n+3])
                line = f.readline()

            print(f"vtxs={len(vtxs)}")
            print(f"txuv={len(txuv)}")
            print(f"norm={len(norm)}")
            print(f"face={len(face)}")
            
            print(f"indx={len(indx)}")
            print(f"indx={indx}")
            print(f"bufr={len(bufr)}")
            print(f"bufr={bufr}")

            indxs = np.array(indx, np.int32)
            vrtxs = np.array(vtxs, np.float32)


if __name__ == '__main__':
    ModelLoader.load_model("res/mdls/Cube.obj")