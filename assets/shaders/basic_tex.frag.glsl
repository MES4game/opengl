#version 330 core

in vec2 frag_texcoord;

uniform sampler2D texture_2D;

out vec4 out_color;

void main() {
    out_color = texture(texture_2D, frag_texcoord);
}
