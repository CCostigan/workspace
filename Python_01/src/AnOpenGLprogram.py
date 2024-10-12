#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr

from TextureLoader import TextureLoader
from ShaderLoader import ShaderLoader
from ModelLoader import ModelLoader
from Interaction import EHandler
from TextWriter import Writer


MIN, MAX = 0.1, 10000.0
model_axis = [0.0, 0.0, 0.0]


class ReviewOpenGL(object):

    def main(self):

        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # glfw.window_hint(glfw.SAMPLES, 1)

        # for m, mon in enumerate(glfw.get_monitors()):
        #     print(f"Monitor {m} = {mon}")
        monitor1 = glfw.get_primary_monitor()
        workarea = glfw.get_monitor_workarea(monitor1)

        print(f"prime_monitor={monitor1} area={workarea}")
        window = glfw.create_window(workarea[2], workarea[3], "Python OpenGL window", monitor1, None) # Fullscreen
        # No window?  Bail
        if not window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")
        
        # fb_size = glfw.get_framebuffer_size(window)
        # glfw.set_window_pos(window, 10, 30)
        glfw.make_context_current(window)
        for monitor in glfw.get_monitors():
            print(f"Monitor Name = {glfw.get_monitor_name(monitor)}")
            print(f"Video Mode={glfw.get_video_mode(monitor)}")
            # print(f"Video Modes={glfw.get_video_modes(monitor)}")

        glfw.maximize_window(window)
        print(f"Vulkan supported = {glfw.vulkan_supported()}")
        # print(f"get_physical_device_presentation_support={glfw.get_physical_device_presentation_support(window)}")
        print(f"Window Opacity={glfw.get_window_opacity(window)}")
        # print(f"Window Attrib={glfw.get_window_attrib(window)}")

        eh = EHandler.configure(window)

        charstrip = TextureLoader.load_texture("res/imgs/charstrip.png")
        ortho_shader = ShaderLoader.load_shader_progs("ortho_vert.glsl","ortho_frag.glsl")

        shaders = []
        shaders.append(ShaderLoader.load_shader_progs("shader_vert.glsl", "shader_frag.glsl"))
        shaders.append(ShaderLoader.load_shader_progs("shader_vert.glsl", "shader_geom0.glsl"))
        shaders.append(ShaderLoader.load_shader_progs("shader_vert.glsl", "shader_geom1.glsl"))
        # shaders.append(ShaderLoader.load_shader_programs("shader_vert.glsl","shader_frag.glsl"))
        # shadrX = ShaderLoader.load_shader_programs("shad_vert.glsl","shad_frag.glsl")
        for shader in shaders:        
            self.setup_shaders(shader)

        textwriter = Writer(workarea)

        ml = ModelLoader()
        models = [
            # ml.model_Elements_HC(),
            # ml.model_Arrays("Cube.obj"),
            # ml.model_Arrays("Cubes4.obj"),
            # ml.model_Arrays("Sphere.obj"),
            ml.model_Arrays("FCA.obj"),
            # ml.model_Arrays("DDG.obj"),
            # ml.model_Arrays("XJ2A1.obj"),
            # ml.model_Arrays("TonyStarkWasAbleToBuildThisInACave-WithABoxOfScrap.obj"),
        ]
        models[0]["location"]=[0.0, 0.0, 0.0]

        modules = [
            ml.model_Arrays("PropellerP.obj"),
            ml.model_Arrays("PropellerS.obj"),
        ]
        # modules[1]["location"]=[0.0, 8.0, 0.0]
        # modules[2]["location"]=[0.0, -8.0, 0.0]
        # models[1]["location"]=[0.0, 6.0, 0.0]
        # models[2]["location"]=[0.0,-3.0, 0.0

        # glUseProgram(shaders[shader_index])
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_BLEND)
        # glEnable(GL_LIGHTING)
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Initial Viewport
        glViewport(workarea[1], workarea[1], workarea[2], workarea[3])

        # self.setup_shaders(shaders[0])

        # the main application loop
        while not glfw.window_should_close(window) and not EHandler.DONE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glfwtime = glfw.get_time()

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

                for module in modules:
                    # glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, model_mtx)
                    # glUniformMatrix4fv(self.uniform_proj, 1, GL_FALSE, EHandler.proj_vec)

                    shaft_end = pyrr.Matrix44.from_translation(pyrr.Vector3([0.0, 0.0, 10.0]))
                    shaft_ang = pyrr.Matrix44.from_y_rotation(0.01 * 90.0) #0.8 * glfwtime)
                    prop_scale = pyrr.Matrix44.from_scale(pyrr.Vector3([0.01, 0.01, 0.01]))
                    prop_angle = pyrr.Matrix44.from_z_rotation(0.01 * 90.0) #0.8 * glfwtime)
                    # pyrr.matrix44.multiply(shaft_end, shaft_ang)
                    # prop_rtn = pyrr.matrix44.multiply(prop_scale, prop_angle)
                    prop_mtx = pyrr.matrix44.multiply(shaft_end, model_mtx) # Move to the end of the shafts
                    prop_mtx = pyrr.matrix44.multiply(prop_mtx, prop_angle)  # Angle the propellers
                    # prop_mtx = pyrr.matrix44.multiply(shaft_ang, model_mtx)
                    # prop_mtx = pyrr.matrix44.multiply(model_mtx, prop_angle)

                    glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, prop_mtx)
                    glUniformMatrix4fv(self.uniform_proj, 1, GL_FALSE, EHandler.proj_vec)                    
                    # glUniformMatrix4fv(self.uniform_modl, 1, GL_FALSE, prop_rtn)
                    # glUniformMatrix4fv(self.uniform_proj, 1, GL_FALSE, EHandler.proj_vec)
                    if module["render"] == "DrawArrays":
                        glBindVertexArray(module["vao"])
                        if len(module["textures"]) > 0:
                            glBindTexture(GL_TEXTURE_2D, module["textures"][0])
                        glDrawArrays(GL_TRIANGLES, 0, len(module["indx"]))

            glfw.swap_buffers(window)
        glfw.terminate()


    def setup_shaders(self, shader):
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



