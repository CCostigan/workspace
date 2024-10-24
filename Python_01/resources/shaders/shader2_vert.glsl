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

//out vec2 vST; // texture coords
//out vec3 vN; // normal vector
out vec3 vL; // vector from point to light
out vec3 vE; // vector from point to eye

void main()
{
//    vST = gl_MultiTexCoord0.st;
    vec4 ECposition = model * vec4(a_position, 1.0); // eye coordinate position
//    vN = normalize( gl_NormalMatrix * gl_Normal ); // normal vector
    vL = light - ECposition.xyz; // vector from the point to the light position
    vE = vec3( 0.0, 0.0, 0.0 ) - ECposition.xyz; // vector from the point to the eye position 
//    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

    gl_Position = proj * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_normal = a_normal;
}
