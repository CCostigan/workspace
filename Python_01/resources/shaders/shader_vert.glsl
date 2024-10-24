#version 330 core

// Some of this from 
//https://sibras.github.io/OpenGL4-Tutorials/docs/Tutorials/03-Tutorial3/

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

out vec3 v_light;      // vector from point to light
out vec3 v_eye;        // vector from point to eye

out vec3 v3ColorOut;

//layout(std140, binding = 3) uniform PointLightData {
//    PointLight PointLights;
//};

void main() {

    v_texture = a_texture;
    v_normal = a_normal;
    gl_Position = m_proj * m_model * vec4(a_position, 1.0);

// https://sibras.github.io/OpenGL4-Tutorials/docs/Tutorials/03-Tutorial3/
// https://www.khronos.org/opengl/wiki/Layout_Qualifier_(GLSL)


    vec4 v4Position = m_model * vec4(a_position, 1.0);
    gl_Position = m_proj * v4Position;

    vec4 v4Normal = m_model * vec4(a_normal, 0.0f);

    vec3 v3Position = v4Position.xyz / v4Position.w;
    vec3 v3Normal = normalize(v4Normal.xyz);
    vec3 v3ViewDirection = normalize(v_eye - v3Position);
//    vec3 v3LightDirection = normalize(PointLights.v3LightPosition - v3Position);
//
    float fRoughness = 0.3;
    vec3 v3SpecularColor = vec3(0.4, 0.4, 0.4);
    vec3 v3DiffuseColor = vec3(0.4, 0.4, 0.4);

//    // Calculate light falloff
//    vec3 v3LightIrradiance = lightFalloff(
//        PointLights.v3LightIntensity, 
//        PointLights.fFalloff, 
//        PointLights.v3LightPosition, v3Position);
// 
//    // Perform shading
//    vec3 v3RetColor = blinnPhong(
//        v3Normal, v3LightDirection, v3ViewDirection, 
//        v3LightIrradiance, v3DiffuseColor, v3SpecularColor, fRoughness);
//
//    v3ColorOut = v3RetColor;

}


vec3 lightFalloff(
    in vec3 v3LightIntensity, 
    in float fFalloff, 
    in vec3 v3LightPosition, 
    in vec3 v3Position) {
    // Calculate distance from light
    float fDist = distance(v3LightPosition, v3Position);
    // Return falloff
    return v3LightIntensity / (fFalloff * fDist * fDist);
}
//
//
vec3 blinnPhong(
    in vec3 v3Normal,
    in vec3 v3LightDirection, 
    in vec3 v3ViewDirection, 
    in vec3 v3LightIrradiance, 
    in vec3 v3DiffuseColor, 
    in vec3 v3SpecularColor, 
    in float fRoughness) { 
    // Calculate half vector
    vec3 v3HalfVector = normalize(v3ViewDirection + v3LightDirection);
    // Calculate specular component
    vec3 v3Specular = pow(max(dot(v3Normal, v3HalfVector), 0.0f), fRoughness) * v3SpecularColor;
    // Combine diffuse and specular
    vec3 v3RetColor = v3DiffuseColor + v3Specular;
    // Multiply by view angle
    v3RetColor *= max(dot(v3Normal, v3LightDirection), 0.0f);
    // Combine with incoming light value
    v3RetColor *= v3LightIrradiance;
    return v3RetColor;
}


