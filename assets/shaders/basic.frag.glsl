#version 330 core

uniform vec3 color_vec3;

out vec4 out_color;

void main() {
    out_color = vec4(color_vec3, 1);
}
