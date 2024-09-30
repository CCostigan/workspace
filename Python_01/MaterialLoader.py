



# https://en.wikipedia.org/wiki/Wavefront_.obj_file#:~:text=The%20Material%20Template%20Library%20format,OBJ%20files.

class MaterialLoader():

    def load_template(template_filename):
        print(f"Opening {template_filename}")  
        with open(template_filename, 'r') as f:
            line = f.readline()
            while line:
                tokens = line.split()
                print(f"Line={tokens}")  
                if len(tokens) == 0:  # Empty line
                    pass
                elif tokens[0] == '#':  # Comment line
                    pass
                elif tokens[0] == "newmtl":  # Material Name
                    pass
                elif tokens[0] == "Ns":  # Specular Highlight
                    pass
                elif tokens[0] == "Ka":  # Ambient Color
                    pass
                elif tokens[0] == "Kd":  # Deliffuse Color
                    pass
                elif tokens[0] == "Ks":  # Specular Color
                    pass
                elif tokens[0] == "Ke":  # Emission Color
                    pass
                elif tokens[0] == "Ni":  # Index of Refraction
                    pass
                elif tokens[0] == "Tr":  # Transmission Color
                    pass
                elif tokens[0] == "d":  # Transmission Color Tr = 1 - d
                    pass
                elif tokens[0] == "Tf":  # Transmission Filter Color
                    pass
                elif tokens[0] == "illum":  # Illumination value?
                    pass
                elif tokens[0] == "map_Kd":  # Filename of Deliffuse texture
                    pass
                elif tokens[0] == "map_Ke":  # Filename of Emission texture
                    pass
                elif tokens[0] == "map_Ks":  # Filename of Specular texture
                    pass
                elif tokens[0] == "map_Ns":  # Filename of Speculat highlight texture
                    pass
                elif tokens[0] == "map_d":   # Filename of Alpha texture
                    pass
                elif tokens[0] == "map_bump":  # Filename of Bumpmap texture
                    pass
                elif tokens[0] == "bump":  # See above
                    pass
                elif tokens[0] == "disp":  # Filename of Displacement texture
                    pass
                elif tokens[0] == "decal":  # Filename of Stencil Decal texture
                    pass
                elif tokens[0] == "refl":  # Filename of Spherical Reflection texture
                    pass
                else:
                    print(f"Unknown objet token {tokens[0]}")
                line = f.readline()

if __name__ == '__main__':
    print("Hello>?")
    material = MaterialLoader.load_template("res/mdls/Cube.mtl")
    print(material)
    # from ReviewOpenGL import ReviewOpenGL
    # ReviewOpenGL.main()