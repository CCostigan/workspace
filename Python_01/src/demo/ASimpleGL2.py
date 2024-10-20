
from OpenGL import GL as gl
import glfw


import ctypes
import contextlib, sys
import numpy as np
import numpy.linalg as linalg

# https://metamost.com/post/tech/opengl-with-python/01-opengl-with-python/

# Above references
# https://www.opengl-tutorial.org/beginners-tutorials/tutorial-3-matrices/

import os
filename, ext = os.path.splitext(os.path.basename(__file__))
import logging as log
log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname).3s] %(message)s",
    handlers=[log.FileHandler(filename+".log"), log.StreamHandler(sys.stdout)],
)


@contextlib.contextmanager
def create_main_window():
    if not glfw.init():
        sys.exit(1)
    try:
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        title = 'Tutorial 2: First Triangle'
        window = glfw.create_window(500, 400, title, None, None)
        if not window:
            sys.exit(2)
        glfw.make_context_current(window)

        glfw.set_input_mode(window, glfw.STICKY_KEYS, True)
        gl.glClearColor(0, 0, 0.4, 0)

        yield window

    finally:
        glfw.terminate()

@contextlib.contextmanager
def create_vertex_array_object():
    vertex_array_id = gl.glGenVertexArrays(1)
    try:
        gl.glBindVertexArray(vertex_array_id)
        yield
    finally:
        gl.glDeleteVertexArrays(1, [vertex_array_id])


@contextlib.contextmanager
def create_vertex_buffer():
    with create_vertex_array_object():

        # A triangle
        vertex_data = [-1, -1, 0,
                        1, -1, 0,
                        0,  1, 0]

        attr_id = 0  # No particular reason for 0, but must match the layout location in the shader.

        vertex_buffer = gl.glGenBuffers(1)
        try:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)

            array_type = (gl.GLfloat * len(vertex_data))
            gl.glBufferData(gl.GL_ARRAY_BUFFER,
                            len(vertex_data) * ctypes.sizeof(ctypes.c_float),
                            array_type(*vertex_data),
                            gl.GL_STATIC_DRAW)

            gl.glVertexAttribPointer(
               attr_id,            # attribute 0.
               3,                  # components per vertex attribute
               gl.GL_FLOAT,        # type
               False,              # to be normalized?
               0,                  # stride
               None                # array buffer offset
            )
            gl.glEnableVertexAttribArray(attr_id)  # use currently bound VAO
            yield
        finally:
            gl.glDisableVertexAttribArray(attr_id)
            gl.glDeleteBuffers(1, [vertex_buffer])



@contextlib.contextmanager
def load_shaders():
    shaders = {
        gl.GL_VERTEX_SHADER: '''\
            #version 330 core
            layout(location = 0) in vec3 vertexPosition_modelspace;
            void main(){
              gl_Position.xyz = vertexPosition_modelspace;
              gl_Position.w = 1.0;
            }
            ''',
        gl.GL_FRAGMENT_SHADER: '''\
            #version 330 core
            out vec3 color;
            void main(){
              color = vec3(1,0,0);
            }
            '''
        }
    program_id = gl.glCreateProgram()
    try:
        shader_ids = []
        for shader_type, shader_src in shaders.items():
            shader_id = gl.glCreateShader(shader_type)
            gl.glShaderSource(shader_id, shader_src)

            gl.glCompileShader(shader_id)

            # check if compilation was successful
            result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
            info_log_len = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
            if info_log_len:
                logmsg = gl.glGetShaderInfoLog(shader_id)
                log.error(logmsg)
                sys.exit(10)

            gl.glAttachShader(program_id, shader_id)
            shader_ids.append(shader_id)

        gl.glLinkProgram(program_id)

        # check if linking was successful
        result = gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS)
        info_log_len = gl.glGetProgramiv(program_id, gl.GL_INFO_LOG_LENGTH)
        if info_log_len:
            logmsg = gl.glGetProgramInfoLog(program_id)
            log.error(logmsg)
            sys.exit(11)

        gl.glUseProgram(program_id)
        yield
    finally:
        for shader_id in shader_ids:
            gl.glDetachShader(program_id, shader_id)
            gl.glDeleteShader(shader_id)
        gl.glUseProgram(0)
        gl.glDeleteProgram(program_id)


def perspective(fov, aspect, near, far):
    n, f = near, far
    t = np.tan((fov * np.pi / 180) / 2) * near
    b = - t
    r = t * aspect
    l = b * aspect
    assert abs(n - f) > 0
    return np.array((
        ((2*n)/(r-l),           0,           0,      0),
        (          0, (2*n)/(t-b),           0,      0),
        ((r+l)/(r-l), (t+b)/(t-b), (f+n)/(n-f),     -1),
        (          0,           0, 2*f*n/(n-f),      0)))

def normalized(v):
    norm = linalg.norm(v)
    return v / norm if norm > 0 else v

def look_at(eye, target, up):
    zax = normalized(eye - target)
    xax = normalized(np.cross(up, zax))
    yax = np.cross(zax, xax)
    x = - xax.dot(eye)
    y = - yax.dot(eye)
    z = - zax.dot(eye)
    return np.array(((xax[0], yax[0], zax[0],    0),
                     (xax[1], yax[1], zax[1],    0),
                     (xax[2], yax[2], zax[2],    0),
                     (     x,      y,      z,    1)))

def main_loop(window):
    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        glfw.swap_buffers(window)
        glfw.poll_events()

if __name__ == '__main__':
    with create_main_window() as window:
        with create_vertex_buffer():
            with load_shaders():
                main_loop(window)

# def main_loop(window):
#     while (
#         glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
#         not glfw.window_should_close(window)
#     ):
#         gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
#         gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
#         glfw.swap_buffers(window)
#         glfw.poll_events()


# if __name__ == '__main__':
#     with create_main_window() as window:
#         with create_vertex_buffer():
#             with load_shaders():
#                 main_loop(window)

# if __name__ == '__main__':
#     with create_main_window() as window:
#         while (
#             glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
#             not glfw.window_should_close(window)
#         ):
#             gl.glClear(gl.GL_COLOR_BUFFER_BIT)
#             glfw.swap_buffers(window)
#             glfw.poll_events()

