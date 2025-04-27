#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec3 frag_light;
in vec2 frag_texcoord;

uniform vec3 light_vec3;
uniform sampler2D texture_2D;

out vec4 out_color;

void main() {
    vec3 ambient = 0.1 * light_vec3;

    vec3 norm = normalize(frag_normal);
    vec3 lightDir = normalize(frag_light - frag_position);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * light_vec3;

    vec3 viewDir = normalize(-frag_position);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = 0.3 * spec * light_vec3;

    vec3 texColor = texture(texture_2D, frag_texcoord).rgb;

    vec3 result = (ambient + diffuse + specular) * texColor;
    out_color = vec4(result, 1);
}
