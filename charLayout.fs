#version 330 core

in vec2 texCoord;
out vec4 FragColor;

uniform sampler2D videoTexture;

uniform float offsetY;
uniform float offsetX;

uniform float bgOpacityF;

void main()
{
    vec2 modUV = texCoord;

    modUV.x /= 10.0;
    modUV.y /= 10.0;

    modUV.y += offsetY;
    modUV.x += offsetX;

    FragColor = texture(videoTexture, modUV.xy);
}
