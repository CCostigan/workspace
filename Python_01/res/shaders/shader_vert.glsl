# version 330

// Actual vertex data 
layout(location = 0) in vec3 a_position;  // Vertex coords
layout(location = 1) in vec2 a_texture;   // Vertex UV coords
layout(location = 2) in vec3 a_normal;    // Vertex normal
//layout(location = 3) in vec3 a_mat;       // Material data

uniform mat4 m_model;  // Model translation rotation scale mtx
uniform mat4 m_proj;   // Projction mtx
uniform vec3 p_light;  // Location of light vec

out vec2 v_texture;
out vec3 v_normal;

out vec3 v_light; // vector from point to light
out vec3 v_eye; // vector from point to eye

void main()
{
//    vST = gl_MultiTexCoord0.st;
    vec4 v_observer = m_model * vec4(a_position, 1.0); // eye coordinate position
//    vN = normalize( gl_NormalMatrix * gl_Normal ); // normal vector
    v_light = p_light - v_observer.xyz; // vector from the point to the light position
    v_eye = vec3( 0.0, 0.0, 0.0 ) - v_observer.xyz; // vector from the point to the eye position 
//    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

    gl_Position = m_proj * m_model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_normal = a_normal;
}
