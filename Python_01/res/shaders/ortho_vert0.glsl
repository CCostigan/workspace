#version 330
// /home/groot/Workspaces/Python/Learn-OpenGL-in-python-master/ep10_orthographic_projection.py

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;

uniform mat4 model; // combined translation and rotation
uniform mat4 projection;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    gl_Position = projection * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
