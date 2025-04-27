#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec3 frag_light;

uniform vec3 light_vec3;
uniform vec3 color_vec3;

out vec4 out_color;

void main() {
    // ambient
    vec3 ambient = 0.1 * light_vec3;

    // diffuse
    vec3 norm = normalize(frag_normal);
    vec3 lightDir = normalize(frag_light - frag_position);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * light_vec3;

    // specular
    vec3 viewDir = normalize(-frag_position);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = 0.3 * spec * light_vec3;

    vec3 result = (ambient + diffuse + specular) * color_vec3;
    out_color = vec4(result, 1);
}
