#version 330 core

// Some of this from 
//https://sibras.github.io/OpenGL4-Tutorials/docs/Tutorials/03-Tutorial3/
// 
in vec2 v_texture;
in vec3 v_normal;
//in vec3 v_frag;
uniform sampler2D s_texture;

in vec3 v_light; // vector from point to light
in vec3 v_eye; // vector from point to eye

uniform mat4 m_model;  // Model translation rotation scale mtx
uniform mat4 m_proj;   // Projction mtx
uniform vec3 p_light;  // Location of light vec

uniform float uKa; // Ambient
uniform float uKd; // Diffuse
uniform float uKs; // Specular
uniform float uKx; // Specular exponent

// Are there any other outputs from a fragment shader?
out vec4 out_color;

void main() {
    vec4  tex_color = texture(s_texture, v_texture);
    vec3  normal = normalize(v_light);
    vec3  eyevec = normalize(v_eye);

    // Ambient Lighting
    vec4  amb_clr = vec4(0.1, 0.1, 0.1,  1.0);

    // Light location & color
    vec3  light_loc = vec3(4.0, 4.0, 4.0);
    vec4  light_clr = vec4(0.8, 0.8, 0.8,  1.0);

    // Diffuse Lighting
    vec4  diff_clr = vec4(0.5, 0.5, 0.5,  1.0); 
    float diff_bri = max(0.0, dot(light_loc, normal));
    vec4  diff_color = diff_bri * light_clr;

    // Specular Lighting
    vec3  spec_vec = normalize(reflect(light_loc, normal));
    float spec_bri = max(0.0, dot(eyevec, spec_vec));
    spec_bri = pow(spec_bri, 48.0);
    vec4  spec_color = spec_bri * light_clr;

    out_color = tex_color;

//    out_color *= amb_clr;
//    out_color *= diff_color;
//    out_color += spec_color;

//    out_color = vec4( tex_color * diff_color )/4;
//    out_color = vec4( tex_color * diff_color * spec_color );

//    out_color = diff_color * spec_color;
//    out_color = tex_color;

//    out_color = blinnPhong(v_normal, v_light, v_eye, light_clr, light_clr, light_clr, 0.5);

//    out_color *= vec4(1.0, 0.0, 0.0, 1.0);// Toggle this to verify shaders are loading
}






