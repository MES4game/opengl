#version 330 core

layout(location = 0) in vec3 vert_position;
layout(location = 1) in vec2 vert_texcoord;
layout(location = 2) in vec3 vert_normal;

uniform mat4 model_mat4;
uniform mat4 view_mat4;
uniform mat4 proj_mat4;
uniform vec3 cam_vec3;

out vec3 frag_position;
out vec3 frag_normal;
out vec3 frag_light;
out vec2 frag_texcoord;

void main() {
    gl_Position = proj_mat4 * view_mat4 * model_mat4 * vec4(vert_position, 1);
    frag_position = vec3(view_mat4 * model_mat4 * vec4(vert_position, 1));
    frag_normal = mat3(transpose(inverse(view_mat4 * model_mat4))) * vert_normal;
    frag_light = vec3(view_mat4 * vec4(cam_vec3, 1));
    frag_texcoord = vert_texcoord;
}
