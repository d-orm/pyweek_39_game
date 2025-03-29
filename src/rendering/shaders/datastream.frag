#version 300 es
precision highp float;
// adapted from https://www.shadertoy.com/view/3lBBWG

out vec4 fragColor;
in vec3 fragCoord;

#include "uniforms"
#include "constants"

// Random function constants
const float RM_X = 32.1231, RM_Y = 2.334, RO = 199.2312, RS = 2412.32312;

// Character constants
const float MAX_CHAR = 15.01, CHAR_SCALE = 3768.0;

// Grid & layout constants
const vec2 CELL_GRID = vec2(8.0, 2.0);
const float CELL_SCALE = 15.0;
const vec2 SMALL_GRID = vec2(15.0, 5.0);
const float SMALL_PAD = 2.0;

// Animation & effect constants
const float SPEED_MULT = 1.0, MIN_SPEED = 0.15, SPEED_SCALE = 0.17;
const float LEN_VAR = 15.0, LEN_OFF = 10.0;
const float U1 = 1.23, U2 = 1.45, U_EXP = 9.0;

// Single random function; overload for float input.
float random(vec2 v) {
    return fract(sin(v.x * RM_X - v.y * RM_Y + RO) * RS);
}
float random(float x) { return random(vec2(x, 0.0)); }

float hue2rgb(float f1, float f2, float h) {
    h = mod(h, 1.0);
    if (6.0 * h < 1.0) return f1 + (f2 - f1) * 6.0 * h;
    if (2.0 * h < 1.0) return f2;
    if (3.0 * h < 2.0) return f1 + (f2 - f1) * (6.0 * ((2.0/3.0) - h));
    return f1;
}

vec3 hsl2rgb(vec3 hsl) {
    if (hsl.y == 0.0)
        return vec3(hsl.z);
    float f2 = (hsl.z < 0.5) ? hsl.z * (1.0 + hsl.y) : hsl.z + hsl.y - hsl.y * hsl.z;
    float f1 = 2.0 * hsl.z - f2;
    return vec3(
        hue2rgb(f1, f2, hsl.x + 1.0/3.0),
        hue2rgb(f1, f2, hsl.x),
        hue2rgb(f1, f2, hsl.x - 1.0/3.0)
    );
}

float character(float index) {
    return (index < MAX_CHAR) ? floor(random(index) * CHAR_SCALE) : 0.0;
}

void main() {
    vec2 grid = CELL_SCALE * CELL_GRID;
    vec2 pixel = fragCoord.xy;
    vec2 cell = floor(pixel * grid);
    
    float offset = random(cell.x);
    float speed = (random(cell.x * 3.0) * SPEED_MULT + MIN_SPEED) * SPEED_SCALE;
    float len = random(cell.x) * LEN_VAR + LEN_OFF;
    
    float prog = mod(cell.y / len + iTime * speed + offset * grid.x, 1.0);
    float effect = 1.0 - 2.0 * U1 * prog * (U2 * prog) * (1.0 - pow(prog, U_EXP));
    
    vec2 smallTotal = SMALL_GRID + vec2(SMALL_PAD);
    vec2 small = floor(fract(pixel * grid) * smallTotal) - vec2(SMALL_PAD);
    
    float symVal = character(floor(random(cell + floor(iTime * speed)) * MAX_CHAR));
    bool inSmall = all(greaterThanEqual(small, vec2(0.0))) &&
                   all(lessThanEqual(small, SMALL_GRID));
    bool draw = inSmall && (mod(floor(symVal / pow(2.0, small.x + small.y * SMALL_GRID.x)), 2.0) == 1.0);
    
    vec3 col = draw ? hsl2rgb(vec3(cell.x / grid.x, 1.0, 0.5)) * effect : vec3(0.0);
    fragColor = vec4(col, 1.0);
}
