#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr
import math
import time
import numpy as np

from TextureLoader import TextureLoader
from ShaderLoader import ShaderLoader
from ModelLoader import ModelLoader
from Interaction import EHandler
from TextWriter import Writer

'''  Logging in Python - According to HAL
Format String Placeholders:
%(asctime)s: Human-readable time when the LogRecord was created.
%(created)f: Time in seconds since the epoch when the LogRecord was created.
%(filename)s: Filename portion of the pathname.
%(funcName)s: Name of the function containing the logging call.
%(levelname)s: Text logging level for the message ('DEBUG', 'INFO', etc.).
%(levelno)d: Numeric logging level for the message (10 for DEBUG, 20 for INFO, etc.).
%(lineno)d: Line number where the logging call was made.
%(message)s: The logged message itself.
%(module)s: Module (name portion of filename).
%(name)s: Name of the logger (useful for filtering).
%(pathname)s: Full pathname of the source file where the logging call was issued.
%(process)d: Process ID.
%(processName)s: Process name.
%(thread)d: Thread ID.
%(threadName)s: Thread name.
We can limit the length of these like so - %(levelname).3s
'''

import logging, os 
from logging import StreamHandler, FileHandler
logbase,ext = os.path.splitext(os.path.basename(__file__))
logging.basicConfig(handlers=[
    StreamHandler(),
    FileHandler(logbase+'.log', mode='w') # The filename:lineno enables hyperlinking
], format='%(asctime)s %(levelname).3s %(filename)s:%(lineno)-4s %(threadName)s %(message)s'
, datefmt='%H:%M:%S'  #  '%Y/%m/%d-%:%M:%S %p'
, level=logging.INFO)

MIN, MAX = 0.1, 10000.0
model_axis = [0.0, 0.0, 0.0]

# fullscreen = True
fullscreen = False

class ReviewOpenGL(object):

    def __init__(self):
        self.log = logging.getLogger(__file__)        

    def main(self):

        if not glfw.init():
            raise Exception("glfw can not be initialized!")


        monitor1 = glfw.get_primary_monitor()
        workarea = glfw.get_monitor_workarea(monitor1)

        self.log.info(f"prime_monitor={monitor1} area={workarea}")
        if fullscreen:
            window = glfw.create_window(workarea[2], workarea[3], "Python OpenGL window", monitor1, None) # Fullscreen
            glfw.maximize_window(window)
        else:
            workarea = [0, 0, 1024, 768]
            window = glfw.create_window(workarea[2], workarea[3], "Python OpenGL window", None, None) # Fullscreen
            glfw.set_window_pos(window, 10, 30)
        # No window?  Bail
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        # glfw.window_hint(glfw.SAMPLES, 1)
        # Tell GLFW we want to use this window as our GL context
        glfw.make_context_current(window)
        # Do some other GL setup
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        glViewport(workarea[1], workarea[1], workarea[2], workarea[3])

        # May need to get the framebuffer size some time
        # fb_size = glfw.get_framebuffer_size(window)
        
        # for monitor in glfw.get_monitors():
        #     self.log.info(f"Monitor Name = {glfw.get_monitor_name(monitor)}")
        #     self.log.info(f"Video Mode={glfw.get_video_mode(monitor)}")
        #     self.log.info(f"Video Modes={glfw.get_video_modes(monitor)}")
        # self.log.info(f"Vulkan supported = {glfw.vulkan_supported()}")
        # self.log.info(f"get_physical_device_presentation_support={glfw.get_physical_device_presentation_support(window)}")
        # self.log.info(f"Window Opacity={glfw.get_window_opacity(window)}")
        # self.log.info(f"Window Attrib={glfw.get_window_attrib(window)}")

        # Set up our handler for Mouse and Keyboard events
        eh = EHandler()
        eh.configure(window)
        # Set up our handler for Shaders
        sl = ShaderLoader() 

        tl = TextureLoader()
        # charstrip = tl.load_texture("res/imgs/charstrip.png")
        ortho_shader = sl.load_shader_progs("ortho_vert.glsl","ortho_frag.glsl")
        textwriter = Writer(workarea)

        shaders = []
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_frag.glsl"))  # Regular view
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_geom0.glsl")) # Wire frame view
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_geom1.glsl")) # Points only view
        for shader in shaders:        
            self.setup_shaders(shader)


        # Load models and modules
        ml = ModelLoader()
        models = [
            # ml.model_Elements_HC(),
            # ml.model_Arrays("Sphere.obj"),
            # ml.model_Arrays("FCA.obj"),
            ml.model_Arrays("DDG.obj"),
        ]
        models[0]["location"]=[0.0, 0.0, 0.0]
        # models[1]["location"]=[0.0, 0.0, 0.0]

        #  Propellers
        props = [
            ml.model_Arrays("PropellerP.obj"),
            ml.model_Arrays("PropellerS.obj"),
        ]
        props[0]["location"]=[ 0.88, 10.7, 0.55]
        props[1]["location"]=[-0.88, 10.7, 0.55]
        shaftrpm=[10.0, -10.0, 0.0, 0.0]
        engineon=[True, True, True, True]

        # Rudders
        rudders = [
            ml.model_Arrays("Rudder.obj"),
            ml.model_Arrays("Rudder.obj"),
        ]
        rudders[0]["location"]=[ 0.8, 11.4, 0.7]
        rudders[1]["location"]=[-0.8, 11.4, 0.7]


        # self.setup_shaders(shaders[0])

        # the main application loop
        revcount=[0.0, 0.0]
        steering=[0.0, 0.0]


        d2r = 3.1415922/180
        # r2d = 1.0/d2r
        # r2d2 = 2*r2d
        shaft_ang = pyrr.Matrix44.from_x_rotation(-90.0 * d2r) 
        prop_scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))
        rudd_scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

        # This horse shit threaded implementation doesn't work
        # sl.start_checking(shaders, "shader_vert.glsl", "shader_frag.glsl")

        # Section 19 of https://sibras.github.io/OpenGL4-Tutorials/docs/Tutorials/03-Tutorial3/
        light = [6.0,5.0,4.0, 1.0,1.0,1.0, 12.5]  # XYZ RGB FALLOFF
        light = np.array(light, np.float32)
        g_uiPointLightUBO = glGenBuffers(1)
        glBindBuffer(GL_UNIFORM_BUFFER, g_uiPointLightUBO)
        glBufferData(GL_UNIFORM_BUFFER, light.nbytes, light, GL_STATIC_DRAW )
        glBindBufferBase(GL_UNIFORM_BUFFER, 2, g_uiPointLightUBO)

        material = [1.0,0.0,0.0, 1.0,0.3,0.3, 15.0]  # ??? ??? ?
        material = np.array(material, np.float32)
        g_uiMaterialUBO = glGenBuffers(1)
        glBindBuffer(GL_UNIFORM_BUFFER, g_uiMaterialUBO)
        glBufferData(GL_UNIFORM_BUFFER, material.nbytes, material, GL_STATIC_DRAW )
        glBindBufferBase(GL_UNIFORM_BUFFER, 3, g_uiMaterialUBO)


        while not glfw.window_should_close(window) and not eh.DONE:

            glfwtime = glfw.get_time()
            # Execute this block roughly every second
            if(int(glfwtime*50) % 50 == 0 ):
                # self.log.info(f"GLFWTIME={glfwtime}")
                # #  This block can be removed if not doing shader development
                if self.check_files("shader_vert.glsl", "shader_frag.glsl"):
                    try:
                        newshader = sl.load_shader_progs("shader_vert.glsl", "shader_frag.glsl")                
                        shaders[0] = newshader
                        self.log.info(f"Shader compiled {newshader}")
                    except Exception as e:
                        self.log.info(f"Exception:{e}")
                        pass
                        

            shaftrpm[0] =  eh.model_data[0]
            shaftrpm[1] = -eh.model_data[0]
            steering[0] = -eh.model_data[1]
            steering[1] = -eh.model_data[1]
            for i in range(0, len(revcount)):
                if engineon[i]:
                    revcount[i] += shaftrpm[i]
                if revcount[i] > 360.0 :
                    revcount[i] -= 360.0
                if revcount[i] < 0.0 :
                    revcount[i] += 360.0
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if textwriter is not None:
                glUseProgram(ortho_shader)
                uniform_mtx_ortho = glGetUniformLocation(ortho_shader, "mtx_ortho")
                glUniformMatrix4fv(uniform_mtx_ortho, 1, GL_FALSE, textwriter.m_ortho)
                textwriter.draw("TEST 1234")

            for model in models:
                # tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -EHandler.DIST]))
                tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([model["location"][0], model["location"][1], -eh.DIST]))
                rot_x = pyrr.Matrix44.from_x_rotation(0.01 * eh.model_axis[0]) #0.0 * glfwtime)
                rot_y = pyrr.Matrix44.from_y_rotation(0.01 * eh.model_axis[1]) #0.8 * glfwtime)
                # rot_z = pyrr.Matrix44.from_z_rotation(0.01 * eh.model_axis[2]) #0.8 * glfwtime)
                rotation_mtx = pyrr.matrix44.multiply(rot_y, rot_x)
                # rotation_mtx = pyrr.matrix44.multiply(rotation_mtx, rot_z)
                model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)

                glUseProgram(shaders[eh.SHADERNUM])
                # glUseProgram(shaders[len(shaders)-1])
                glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, model_mtx)
                glUniformMatrix4fv(self.uniform_proj, 1, GL_FALSE, eh.proj_vec)

                if model["render"] == "DrawArrays":
                    glBindVertexArray(model["vao"])
                    if len(model["textures"]) > 0:
                        glBindTexture(GL_TEXTURE_2D, model["textures"][0])
                    glDrawArrays(GL_TRIANGLES, 0, len(model["indx"]))
                # if model["render"] == "DrawElements":
                #     glBindBuffer(GL_ARRAY_BUFFER, model["vbo"])
                #     glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model["ebo"])
                #     glBindTexture(GL_TEXTURE_2D, model["textures"][0])
                #     glDrawElements(GL_TRIANGLES, len(model["indx"]), GL_UNSIGNED_INT, None)

                for m, prop in enumerate(props):
                    d2r = 3.1415922/180
                    # shaft_end = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 3.5, 1.3]))
                    shaft_end = pyrr.matrix44.create_from_translation(pyrr.Vector3([prop["location"][0], prop["location"][1], prop["location"][2]]))
                    prop_angle = pyrr.Matrix44.from_y_rotation(revcount[m] * d2r)
                    # Accumulate the matrices for the propeller(s
                    prop_mtx = model_mtx # Copy the Model matrix to the prop matrix, this is just for convenience 
                    prop_mtx = pyrr.matrix44.multiply(shaft_ang, prop_mtx)   # Angle the prop to the shaft
                    prop_mtx = pyrr.matrix44.multiply(shaft_end, prop_mtx)   # Move prop to end of shaft
                    prop_mtx = pyrr.matrix44.multiply(prop_angle, prop_mtx)  # Turn the propeller
                    prop_mtx = pyrr.matrix44.multiply(prop_scale, prop_mtx)  # Scale the propeller

                    glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, prop_mtx)
                    if prop["render"] == "DrawArrays":
                        glBindVertexArray(prop["vao"])
                        if len(prop["textures"]) > 0:
                            glBindTexture(GL_TEXTURE_2D, prop["textures"][0])
                        glDrawArrays(GL_TRIANGLES, 0, len(prop["indx"]))

                for r, rudder in enumerate(rudders):
                    # shaft_end = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 3.5, 1.3]))
                    shaft_end = pyrr.matrix44.create_from_translation(pyrr.Vector3([rudder["location"][0], rudder["location"][1], rudder["location"][2]]))
                    rudd_angle = pyrr.Matrix44.from_z_rotation(steering[r] * d2r)
                    # Acccumulate the matrices for the rudder(s)
                    rudd_mtx = model_mtx # Copy the Model matrix to the rudder matrix, this is just for convenience 
                    rudd_mtx = pyrr.matrix44.multiply(shaft_ang, rudd_mtx)   # Angle the rudder to the shaft
                    rudd_mtx = pyrr.matrix44.multiply(shaft_end, rudd_mtx)   # Move rudder to end of shaft
                    rudd_mtx = pyrr.matrix44.multiply(rudd_angle, rudd_mtx)  # Turn the rudder
                    rudd_mtx = pyrr.matrix44.multiply(rudd_scale, rudd_mtx)  # Scale the rudder

                    glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, rudd_mtx)
                    if rudder["render"] == "DrawArrays":
                        glBindVertexArray(rudder["vao"])
                        if len(rudder["textures"]) > 0:
                            glBindTexture(GL_TEXTURE_2D, rudder["textures"][0])
                        glDrawArrays(GL_TRIANGLES, 0, len(rudder["indx"]))

            glfw.swap_buffers(window)
        glfw.terminate()
        sl.stop_checking()

    def check_files(self, *filelist):
        reload = False
        shader_home="res/shaders/"
        for filename in filelist:
            stats_mt = os.stat(shader_home+filename).st_mtime        
            if stats_mt > self.last_update:
                self.last_update = time.time()
                reload = True
        return reload

    def setup_shaders(self, shader):
        self.last_update = time.time()
        glUseProgram(shader)
        self.uniform_modl = glGetUniformLocation(shader, "m_model")
        self.uniform_proj = glGetUniformLocation(shader, "m_proj")
        self.uniform_LP = glGetUniformLocation(shader, "p_light")
        self.uniform_Ka = glGetUniformLocation(shader, "uKa")
        self.uniform_Kd = glGetUniformLocation(shader, "uKd")
        self.uniform_Ks = glGetUniformLocation(shader, "uKs")
        self.uniform_Sh = glGetUniformLocation(shader, "uKx")
        glUniform3fv(self.uniform_LP, 1, GL_FALSE, pyrr.Vector3([5.0, 5.0, 0.0]))
        glUniform1fv(self.uniform_Ka, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Kd, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Ks, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Sh, 1, GL_FALSE, 0.1)
        pass


if __name__=='__main__':
    program = ReviewOpenGL()
    program.main()



