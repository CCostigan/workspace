

    
# Blender importer
    /usr/share/blender/scripts/templates_py/operator_file_import.py

# OpenGL tutorials
    https://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/

# Math for GL
    https://www.3dgep.com/3d-math-primer-for-game-programmers-matrices/

# Some good info (even though they are using garbage JS)
    https://www.youtube.com/watch?v=3mfvZ-mdtZQ


# Shader parameters
-Uniform   - read only - constant
-Attribute - read only - 1:1 vretices
-Varying   - read/write in the vertex shader, read only in the frag



# Docker to Podman 
    https://metamost.com/post/tech/podman-from-docker-compose/


# Circular repetition stuff - arrays
https://www.youtube.com/watch?v=ejR1_JzFDKY

# Propellers
https://www.navsea.navy.mil/Home/Shipyards/Norfolk/Department-Links/Naval-Foundry-and-Propeller-Center/
https://www.youtube.com/watch?v=rLcZhsNQR4Q
https://www.youtube.com/watch?v=OEDFDQFsXiE
https://www.youtube.com/watch?v=ZmI1gBAyUok
https://www.youtube.com/watch?v=HGL6QpVRyXk

# Topology (Welding)
https://www.youtube.com/watch?v=m8JkR6tI_q4


# Python ASYNC IO
https://docs.python.org/3/library/asyncio-stream.html#asyncio-streams

# DDS pretending to actually work
https://community.rti.com/static/documentation/connext-dds/6.0.1/api/connext_dds/api_python/types.html#defining-types-programmatically
https://community.rti.com/static/documentation/connext-dds/6.0.1/api/connext_dds/api_python/types.html#accessing-nested-members

# Cameo admiting they suck ass - please debug our piece of shit for us
https://docs.nomagic.com/display/FAQ/I+suspect+a+performance+problem.+How+do+I+solve+it


# Propeller instructions
    Add Empty spehere at origin
    Add UV Sphere and RY90 
        move on +X axis so point is on origin
        flatten it on the X-Z plane (Surfboard)
        Mesh Transform Bend to your liking
        Taper X ~1.8
        Twist X ~85
        Arrary X Object Offset Empty

# Phong Shading -- nice demo
    https://www.youtube.com/watch?v=LKXAIuCaKAQ
    https://gamedev.stackexchange.com/questions/89787/opengl-light-appears-to-move-with-camera-and-changes-with-object-rotation




# GREAT Explanation
https://gamedev.stackexchange.com/questions/89787/opengl-light-appears-to-move-with-camera-and-changes-with-object-rotation

    From what I read from the shaders the light is in world-space and the light calculation is done on the object in part in untransformed object-space.

    You need to compute your lighting with both light & model in world-space or both in camera space.

    Whenever moving the camera messes up the lighting it means some of the data is calculated in a different space from the rest.

    (a_vertexPosition.xyz) 
    is in object space (before the object is placed in the 3D world).

    (a_vertexPosition.xyz * modelmatrix) 
    is in world space.

    ((a_vertexPosition.xyz * modelmatrix) * viewmatrix) 
    is in view (camera) space.

    (((a_vertexPosition.xyz * modelmatrix) * viewmatrix) * projectionmatrix) 
    is in screen space (just before perspective).

    vec4 temp = ((a_vertexPosition.xyz * modelmatrix) * viewmatrix) * projectionmatrix;
    temp /= temp.w; 
    is in projected screen space. The GPU does this division by w just before the pixel shader. Sometimes you need to calculate this in the vertex shader to do 2D effects.