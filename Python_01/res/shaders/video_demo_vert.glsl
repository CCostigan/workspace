#version 330 core

attribute vec3 aPosition;
attribute vec2 aTexCoord;

varying vec3 pos;

void main() {
    pos = aTexCoord;
    vec3 position = vec4(aPosition, 1.0);
    position.xy = position.xy * 2.0 -1.0;

    gl_Position = position;
}
