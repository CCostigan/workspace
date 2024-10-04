#version 330

layout (triangles) in;
// Render Lines
layout (line_strip, max_vertices=3) out;
// Render Points
//layout (points, max_vertices=3) out;

in vec2 texcoords_pass[]; // texcoords from Vertex Shader
in vec3 normals_pass[]; // normals from Vertex Shader

out vec3 normals; // normals for Fragment Shader
out vec2 texcoords; // texcoords for Fragment Shader

void main(void)
{
    int i;
    for (i = 0; i < gl_in.length(); i++)
    {
        texcoords=texcoords_pass[i]; // pass through
        normals=normals_pass[i]; // pass through
        gl_Position = gl_in[i].gl_Position; // pass through
        EmitVertex();
    }
    EndPrimitive();
}
