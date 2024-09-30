# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model; // combined translation and rotation
uniform mat4 proj;
uniform vec3 light;  

out vec3 v_color;
out vec2 v_texture;
out vec3 v_normal;

void main()
{
    gl_Position = proj * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_normal = a_normal;
}
