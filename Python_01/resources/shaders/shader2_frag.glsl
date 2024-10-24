# version 330

in vec2 v_texture;
in vec3 v_normal;
//in vec3 v_frag;

out vec4 out_color;

uniform sampler2D s_texture;


uniform float uKa; // coefficients of each type of lighting 
uniform float uKd; // coefficients of each type of lighting 
uniform float uKs; // coefficients of each type of lighting
uniform float uShininess; // specular exponent
//in vec2 vST; // texture cords
//in vec3 vN; // normal vector
in vec3 vL; // vector from point to light
in vec3 vE; // vector from point to eye

void main()
{
//    out_color = texture(s_texture, v_texture);

    vec3 Normal = normalize(v_normal);
    vec3 Light = normalize(vL);
    vec3 Eye = normalize(vE);

    vec4 myColor = texture(s_texture, v_texture);//vec4( 1.0, 0.5, 0.0, 1.0 ); // default color
    vec4 mySpecularColor = vec4( 1.0, 1.0, 1.0, 1.0 ); // specular highlight color

    vec4 ambient = myColor;//uKa * myColor;
    float d = 0.0;
    float s = 0.0;
    if( dot(Normal,Light) > 0.0 ) {// only do specular if the light can see the point
        d = dot(Normal,Light);
        vec3 ref = normalize( reflect( -Light, Normal ) ); // reflection vectors = pow( max( dot(Eye,ref),0. ), uShininess );
    }
    vec4 diffuse = uKd * d * myColor;
    vec4 specular = uKs * s * mySpecularColor;
    out_color = vec4( ambient + diffuse + specular );///texture(s_texture, v_texture);
}
