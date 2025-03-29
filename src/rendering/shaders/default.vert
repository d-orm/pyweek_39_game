#version 300 es
precision highp float;

layout (location = 0) in vec2 in_vert;
layout (location = 1) in vec2 in_tex;

layout (location = 2) in vec4 in_rect;
layout (location = 3) in float in_rot;
layout (location = 4) in float in_tex_idx;
layout (location = 5) in float in_depth;

out vec3 fragCoord;

#include "constants"
#include "uniforms"

struct Rect {
    vec2 pos;
    vec2 size;
};

mat4 orthoMatrix = mat4(
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, -1, 0,
    0, 0, 0, 1
);

vec2 rotate(vec2 vert, float angle) {
    float rad = radians(angle);
    mat2 rot = mat2(cos(rad), -sin(rad), sin(rad), cos(rad));
    return rot * vert;
}

Rect rectToNDC(vec4 rect, vec2 screenSize) {
    float ndcX = (rect.x / screenSize.x) * 2.0 - 1.0;
    float ndcY = (-rect.y / screenSize.y) * 2.0 + 1.0;
    float ndcW = (rect.z / screenSize.x) * 2.0;
    float ndcH = (rect.w / screenSize.y) * 2.0;
    return Rect(vec2(ndcX, ndcY), vec2(ndcW, ndcH));
}

void main() {
    Rect rect = rectToNDC(in_rect, iResolution);
    rect.pos.y -= rect.size.y;
    vec2 centeredVert = (in_vert - vec2(0.5, -0.5)) * in_rect.zw;
    vec2 rotVert = rotate(centeredVert, in_rot);
    rotVert = (rotVert / in_rect.zw) + vec2(0.5, 0.5);
    float normalizedDepth = (in_depth / 1000.0) - 1.0;
    vec4 ndcPosition = vec4(rect.pos + (rotVert * rect.size), normalizedDepth, 1.0);
    gl_Position = orthoMatrix * ndcPosition;
    fragCoord = vec3(in_tex, in_tex_idx);
}
