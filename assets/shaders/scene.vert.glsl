#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texcoord;
layout(location = 2) in vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 frag_color;

void main() {
    gl_Position = projection * view * model * vec4(position, 1);
    frag_color = position;
}
