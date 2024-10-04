#!~/.venv/bin/python


from OpenGL.GL import *
import glfw
import pyrr

from TextureLoader import TextureLoader
from ShaderLoader import ShaderLoader
from ModelLoader import ModelLoader
from Interaction import EHandler
from TextWriter import Writer


WIDTH, HEIGHT = 1600, 900
MIN, MAX = 0.1, 10000.0
model_axis = [0.0, 0.0, 0.0]

class ReviewOpenGL(object):

    def main():

        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        # glfw.window_hint(glfw.SAMPLES, 1)

        # creating the window


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

        shader = ShaderLoader.load_shader_programs("shader_vert.glsl","shader_frag.glsl")
        shadr2 = ShaderLoader.load_shader_programs("sh_vert.glsl","sh_frag.glsl")

        textwriter = Writer()

        ml = ModelLoader()
        models = [
            # ml.model_Elements_HC(),
            # ml.model_Elements("res/mdls/Cube.obj"),
            # ml.model_Arrays("res/mdls/FCA.obj"),
            # ml.model_Arrays("res/mdls/Cube.obj"),
            ml.model_Arrays("res/mdls/DDG.obj"),
        ]

        # charstrip = TextureLoader.load_texture("res/imgs/charstrip.png")
        # models[0]["textures"].append(TextureLoader.load_texture("res/imgs/lena.jpg"))
        models[0]["textures"].append(TextureLoader.load_texture("res/imgs/ddg0.png"))
        # models[0]["textures"].append(TextureLoader.load_texture("res/imgs/pic1.png"))
        
        models[0]["location"]=[0.0, 0.0, 0.0]
        # models[1]["location"]=[0.0, 6.0, 0.0]
        # models[2]["location"]=[0.0,-3.0, 0.0]


        glUseProgram(shader)
        glClearColor(0.1, 0.2, 0.4, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        # glEnable(GL_LIGHTING)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Initial Viewport
        glViewport(0, 0, WIDTH, HEIGHT)

        # Talk to the shaders
        uniform_modl = glGetUniformLocation(shader, "m_model")
        uniform_proj = glGetUniformLocation(shader, "m_proj")
        # Lighting
        uniform_LP = glGetUniformLocation(shader, "p_light")
        uniform_Ka = glGetUniformLocation(shader, "uKa")
        uniform_Kd = glGetUniformLocation(shader, "uKd")
        uniform_Ks = glGetUniformLocation(shader, "uKs")
        uniform_Sh = glGetUniformLocation(shader, "uShininess")
        # https://web.engr.oregonstate.edu/~mjb/cs557/Handouts/lighting.1pp.pdf
        glUniform3fv(uniform_LP, 1, GL_FALSE, pyrr.Vector3([5.0, 5.0, 0.0]))
        glUniform1fv(uniform_Ka, 1, GL_FALSE, 0.1)
        glUniform1fv(uniform_Kd, 1, GL_FALSE, 0.1)
        glUniform1fv(uniform_Ks, 1, GL_FALSE, 0.1)
        glUniform1fv(uniform_Sh, 1, GL_FALSE, 0.1)

        # the main application loop
        while not glfw.window_should_close(window) and not EHandler.DONE:
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glfwtime = glfw.get_time()

            if textwriter is not None:
                glUseProgram(shadr2)
                uniform_mtx_ortho = glGetUniformLocation(shadr2, "mtx_ortho")
                glUniformMatrix4fv(uniform_mtx_ortho, 1, GL_FALSE, textwriter.m_ortho)
                textwriter.draw("TEST 1234")

            for model in models:
                glUseProgram(shader)
                # tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, 0.0, -EHandler.DIST]))
                tran_vec = pyrr.matrix44.create_from_translation(pyrr.Vector3([model["location"][0], model["location"][1], -EHandler.DIST]))
                rot_x = pyrr.Matrix44.from_x_rotation(0.01 * EHandler.model_axis[0]) #0.0 * glfwtime)
                rot_y = pyrr.Matrix44.from_y_rotation(0.01 * EHandler.model_axis[1]) #0.8 * glfwtime)
                # rot_z = pyrr.Matrix44.from_z_rotation(0.01 * EHandler.model_axis[2]) #0.8 * glfwtime)
                rotation_mtx = pyrr.matrix44.multiply(rot_y, rot_x)
                # rotation_mtx = pyrr.matrix44.multiply(rotation_mtx, rot_z)
                model_mtx = pyrr.matrix44.multiply(rotation_mtx, tran_vec)
                glUniformMatrix4fv(uniform_modl, 1, GL_FALSE, model_mtx)
                glUniformMatrix4fv(uniform_proj, 1, GL_FALSE, EHandler.proj_vec)
                if model["render"] == "DrawElements":
                    glBindBuffer(GL_ARRAY_BUFFER, model["vbo"])
                    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, model["ebo"])
                    glBindTexture(GL_TEXTURE_2D, model["textures"][0])
                    glDrawElements(GL_TRIANGLES, len(model["indx"]), GL_UNSIGNED_INT, None)
                if model["render"] == "DrawArrays":
                    glBindVertexArray(model["vao"])
                    if len(model["textures"]) > 0:
                        glBindTexture(GL_TEXTURE_2D, model["textures"][0])
                    glDrawArrays(GL_TRIANGLES, 0, len(model["indx"]))

            glfw.swap_buffers(window)
        glfw.terminate()


if __name__=='__main__':
    ReviewOpenGL.main()



