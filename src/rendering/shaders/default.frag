#version 300 es
precision highp float;
precision highp sampler2DArray;

uniform sampler2DArray Texture0;

layout (location = 0) out vec4 fragColor;

in vec3 fragCoord;

#include "uniforms"

void main() {
    vec4 color = texture(Texture0, fragCoord);
    if (color.a == 0.0) {
        discard;
    }
    fragColor = color;
}