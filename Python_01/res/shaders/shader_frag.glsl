# version 330

in vec2 v_texture;
in vec3 v_normal;
//in vec3 v_frag;
uniform sampler2D s_texture;

in vec3 v_light; // vector from point to light
in vec3 v_eye; // vector from point to eye

uniform float uKa; // Ambient
uniform float uKd; // Diffuse
uniform float uKs; // Specular
uniform float uShininess; // Specular exponent

// Are there any other outputs from a fragment shader?
out vec4 out_color;

void main()
{
//    out_color = texture(s_texture, v_texture);  //  Just plain texture color

    vec4 v_color = texture(s_texture, v_texture);//vec4( 1.0, 0.5, 0.0, 1.0 ); // default color
    vec4 v_spec_color = vec4( 1.0, 1.0, 1.0, 1.0 ); // specular highlight color

    vec4 v_ambient = v_color;//uKa * myColor;
    float d = 0.0;
    float s = 0.0;
    if( dot(v_normal,v_light) > 0.0 ) {// only do specular if the light can see the point
        d = dot(v_normal,v_light);
        vec3 ref = normalize( reflect( -v_light, v_normal ) ); // reflection vectors = pow( max( dot(Eye,ref),0. ), uShininess );
    }
    vec4 v_diffuse = uKd * d * v_color;
    vec4 v_specular = uKs * s * v_spec_color;
    out_color = vec4( v_ambient + v_diffuse + v_specular );///texture(s_texture, v_texture);
}
