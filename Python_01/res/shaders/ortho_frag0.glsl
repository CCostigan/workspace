#version 330
// /home/groot/Workspaces/Python/Learn-OpenGL-in-python-master/ep10_orthographic_projection.py
in vec2 v_texture;
out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
