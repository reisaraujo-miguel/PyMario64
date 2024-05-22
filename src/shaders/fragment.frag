#version 330 core

precision mediump float;

uniform vec4 color;
varying vec2 out_texture;
uniform sampler2D samplerTexture;

void main() {
    vec4 texture = texture2D(samplerTexture, out_texture);

    if (texture.a != 1.0f) {
        discard;
    }

    gl_FragColor = texture;
}
