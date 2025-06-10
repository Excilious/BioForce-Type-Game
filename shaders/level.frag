#version 330 core

out vec4 frag_color;

in vec2 uv;
in float shading;
flat in int tex_id;
in vec3 frag_pos;
in vec3 frag_normal;

const vec3 gamma = vec3(4.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray u_texture_array_0;
// Removed unused uniform vec3 extralight;
uniform vec3 light_pos;
uniform vec3 light_color;
uniform vec3 view_pos;

void main() {
    vec3 tex_col = texture(u_texture_array_0, vec3(uv, tex_id)).rgb;
    tex_col = pow(tex_col, gamma);

    // Compute lighting
    vec3 norm = normalize(frag_normal);
    if (length(norm) < 0.001) norm = vec3(0.0, 0.0, 1.0); // Fallback normal

    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0.0); // Standard diffuse lighting
    
    // Strong Point Light Attenuation
    float distance = length(light_pos - frag_pos);
    float attenuation = 1.0 / (1.0 + 0.2 * distance + 0.1 * distance * distance); // Stronger falloff
    vec3 lighting = light_color * diff * attenuation * 5.0; // Make light concentrated
    
    // Ensure the scene is dark except for the lighted spot
    tex_col *= lighting;
    tex_col = pow(tex_col, inv_gamma);

    frag_color = vec4(tex_col, 1.0);
}
