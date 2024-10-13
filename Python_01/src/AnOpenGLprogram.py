#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr
import math
import os
import time

from TextureLoader import TextureLoader
from ShaderLoader import ShaderLoader
from ModelLoader import ModelLoader
from Interaction import EHandler
from TextWriter import Writer


MIN, MAX = 0.1, 10000.0
model_axis = [0.0, 0.0, 0.0]

# fullscreen = True
fullscreen = False

class ReviewOpenGL(object):

    def main(self):

        if not glfw.init():
            raise Exception("glfw can not be initialized!")


        monitor1 = glfw.get_primary_monitor()
        workarea = glfw.get_monitor_workarea(monitor1)

        print(f"prime_monitor={monitor1} area={workarea}")
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
        #     print(f"Monitor Name = {glfw.get_monitor_name(monitor)}")
        #     print(f"Video Mode={glfw.get_video_mode(monitor)}")
        #     print(f"Video Modes={glfw.get_video_modes(monitor)}")
        # print(f"Vulkan supported = {glfw.vulkan_supported()}")
        # print(f"get_physical_device_presentation_support={glfw.get_physical_device_presentation_support(window)}")
        # print(f"Window Opacity={glfw.get_window_opacity(window)}")
        # print(f"Window Attrib={glfw.get_window_attrib(window)}")

        # Set up our handler for Mouse and Keyboard events
        eh = EHandler.configure(window)
        # Set up our handler for Shaders
        sl = ShaderLoader()

        charstrip = TextureLoader.load_texture("res/imgs/charstrip.png")
        ortho_shader = sl.load_shader_progs("ortho_vert.glsl","ortho_frag.glsl")

        shaders = []
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_frag.glsl"))  # Regular view
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_geom0.glsl")) # Wire frame view
        shaders.append(sl.load_shader_progs("shader_vert.glsl", "shader_geom1.glsl")) # Points only view
        # Start the monitor thread to detect changes to shader files.  This would only be used in dev env
        sl.start_checking(shaders, "shader_vert.glsl", "shader_frag.glsl")
        for shader in shaders:        
            self.setup_shaders(shader)

        textwriter = Writer(workarea)

        # Load models and modules
        ml = ModelLoader()
        models = [
            # ml.model_Elements_HC(),
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
        shaft_ang = pyrr.Matrix44.from_x_rotation(-90.0 * d2r) 
        prop_scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))
        rudd_scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.1, 0.1, 0.1]))

        while not glfw.window_should_close(window) and not EHandler.DONE:
            glfwtime = glfw.get_time()

            #  This block can be removed if not doing shader development
            if self.check_files("shader_vert.glsl", "shader_frag.glsl"):
                try:
                    newshader = sl.load_shader_progs("shader_vert.glsl", "shader_frag.glsl")                
                    shaders[0] = newshader
                except Exception as e:
                    pass

            # ShaderLoader.check_shaders()
            # print(f"GLFWTIME={glfwtime}")
            steering[0] = 30.0 * math.sin(glfwtime)
            steering[1] = 30.0 * math.sin(glfwtime)
            for i in range(0, len(revcount)):
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
                tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([model["location"][0], model["location"][1], -EHandler.DIST]))
                rot_x = pyrr.Matrix44.from_x_rotation(0.01 * EHandler.model_axis[0]) #0.0 * glfwtime)
                rot_y = pyrr.Matrix44.from_y_rotation(0.01 * EHandler.model_axis[1]) #0.8 * glfwtime)
                # rot_z = pyrr.Matrix44.from_z_rotation(0.01 * EHandler.model_axis[2]) #0.8 * glfwtime)
                rotation_mtx = pyrr.matrix44.multiply(rot_y, rot_x)
                # rotation_mtx = pyrr.matrix44.multiply(rotation_mtx, rot_z)
                model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)

                glUseProgram(shaders[EHandler.SHADERNUM])
                # glUseProgram(shaders[len(shaders)-1])
                glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, model_mtx)
                glUniformMatrix4fv(self.uniform_proj, 1, GL_FALSE, EHandler.proj_vec)

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
        self.uniform_Sh = glGetUniformLocation(shader, "uShininess")
        glUniform3fv(self.uniform_LP, 1, GL_FALSE, pyrr.Vector3([5.0, 5.0, 0.0]))
        glUniform1fv(self.uniform_Ka, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Kd, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Ks, 1, GL_FALSE, 0.1)
        glUniform1fv(self.uniform_Sh, 1, GL_FALSE, 0.1)
        pass


if __name__=='__main__':
    program = ReviewOpenGL()
    program.main()



