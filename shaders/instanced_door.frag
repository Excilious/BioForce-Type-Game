#version 330 core

out vec4 frag_color;

in vec2 uv;
flat in int tex_id;
uniform vec3 extralight;
uniform sampler2DArray u_texture_array_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;


void main() {
    vec3 tex_col = texture(u_texture_array_0, vec3(uv, tex_id)).rgb;
    tex_col = pow(tex_col, gamma);

    // fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    tex_col = mix(tex_col, vec3(-0.1), (1.0 - exp2(-0.015 * fog_dist * fog_dist)));

    tex_col = pow(tex_col, inv_gamma);
    tex_col *= extralight;
    frag_color = vec4(tex_col, 1.0);
}