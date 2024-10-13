#version 330 core

// 
in vec2 v_texture;
in vec3 v_normal;
//in vec3 v_frag;
uniform sampler2D s_texture;

in vec3 v_light; // vector from point to light
in vec3 v_eye; // vector from point to eye

uniform float uKa; // Ambient
uniform float uKd; // Diffuse
uniform float uKs; // Specular
uniform float uKx; // Specular exponent

// Are there any other outputs from a fragment shader?
out vec4 out_color;

void main() {
    vec4  tex_color = texture(s_texture, v_texture);//vec4( 1.0, 0.5, 0.0, 1.0 ); // default color
    vec3  normal = normalize(v_normal.xyz);
    vec3  eyevec = normalize(v_eye);

    // Ambient Lighting
    vec4  amb_clr = vec4(1.0, 1.0, 1.0, 1.0);

    // Diffuse Lighting
    vec3  diff_loc = v_light;//vec3(1.0, 0.0, 0.0);
    vec4  diff_clr = vec4(1.0,0.0, 0.0, 1.0); 
    float diff_str = max(0.0, dot(diff_loc, normal));
    vec4  diff_color = diff_str * diff_clr;

    // Specular Lighting
    vec3  refl_vec = normalize(reflect(-diff_loc, normal));
    float spec_str = max(0.0, dot(eyevec, refl_vec));
    spec_str = pow(spec_str, 2.0);
//    vec4 v_ambient = v_color;//uKa * myColor;
//    float d = 0.0;
//    float s = 0.0;
//    if( dot(v_normal,v_light) > 0.0 ) {// only do specular if the light can see the point
//        d = dot(v_normal,v_light);
//        vec3 ref = normalize( reflect( -v_light, v_normal ) ); // reflection vectors = pow( max( dot(Eye,ref),0. ), uShininess );
//    }
//    vec4 v_diffuse = uKd * d * v_color;
//    vec4 v_specular = uKs * s * v_spec_color;
//    out_color = vec4( v_ambient + v_diffuse + v_specular );///texture(s_texture, v_texture);
    out_color = tex_color;//spec_str * tex_color * diff_color;
}

//void old_main() {
//    out_color = texture(s_texture, v_texture);  //  Just plain texture color
//}

