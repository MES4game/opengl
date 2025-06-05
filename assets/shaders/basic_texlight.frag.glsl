#version 330 core

#define MAX_LIGHTS 50

in vec3 frag_position;
in vec3 frag_normal;
in vec3 frag_view_pos;
in vec2 frag_texcoord;

uniform vec3 light_positions[MAX_LIGHTS];
uniform vec3 light_colors[MAX_LIGHTS];
uniform int num_lights;

uniform sampler2D texture_2D;

out vec4 out_color;

void main() {
    vec3 norm = normalize(frag_normal);
    vec3 view_dir = normalize(frag_view_pos - frag_position);
    vec3 tex_color = texture(texture_2D, frag_texcoord).rgb;

    vec3 result = vec3(0.0);

    for (int i = 0; i < num_lights; i++) {
        vec3 light_dir = normalize(light_positions[i] - frag_position);

        // Ambient
        vec3 ambient = 0.1 * light_colors[i];

        // Diffuse
        float diff = max(dot(norm, light_dir), 0.0);
        vec3 diffuse = diff * light_colors[i];

        // Specular
        vec3 reflect_dir = reflect(-light_dir, norm);
        float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
        vec3 specular = 0.3 * spec * light_colors[i];

        vec3 lighting = ambient + diffuse + specular;
        result += lighting;
    }

    out_color = vec4(result * tex_color, 1.0);
}
