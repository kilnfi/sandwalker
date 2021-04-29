{% raw %}
#ifdef GL_ES
precision highp float;
#endif

uniform float time;
uniform float scaleFactor;
uniform float rndSeed;
uniform vec2 resolution;

#define CIRCLES 40
#define SPEED 0.4

float rnd(float x) {
  return fract(sin(dot(vec2(x + 10.07, 4.247 / (x + 2.)), vec2(12.9898, 78.233))) * (43758.5453 * rndSeed));
}

float drawCircle(vec2 uv, vec2 center, float radius) {
  return 1.0 - smoothstep(radius / 2.0, radius, length(uv - center));
}

void main() {
  vec2 uv = gl_FragCoord.xy / resolution.xy;
  vec2 sq = gl_FragCoord.xy / resolution.x;
  vec4 bg = vec4(0.203125, 0.19140625, 0.19140625, 1.0);
  vec4 color;

  color = bg;
 
  for(int i = 0; i < CIRCLES; i++) {
    float j = float(i);
    float speed = (0.2 * rnd(cos(j)) - 0.05) * SPEED;
    float circle_radius = max(0.01, rnd(j + 1.0) * 0.12) * scaleFactor;
    vec4 circle_color = vec4(rnd(j), rnd(j + 1.0), rnd(j + 2.0), rnd(j + 3.0) * 0.1);
    vec2 pos = vec2((sq.y * 0.1 + rnd(j)), mod(sin(j) + speed * (time * 0.3), 1.0));

    // This is a windows related hack as we can't compute negative
    // length under webgl there.
    vec2 offset = vec2(0.0, 0.25);

    color += circle_color * drawCircle(sq + offset, pos, circle_radius);
  }

  gl_FragColor = color;
}
{% endraw %}
