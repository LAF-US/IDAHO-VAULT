#version 330 core

in vec2 texCoord;
out vec4 FragColor;

uniform sampler2D videoTexture;

uniform float offsetY;
uniform float numGlyphsF;

uniform float bgOpacityF;

void main()
{
    vec2 modUV = texCoord;

    modUV.y /= numGlyphsF;
    modUV.y += offsetY;

    FragColor = texture(videoTexture, modUV.xy);
}
