#version 330 core

attribute vec3 position;
attribute vec2 texture_coord;
varying vec2 out_texture;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(position,1.0);
    out_texture = vec2(texture_coord);
}
