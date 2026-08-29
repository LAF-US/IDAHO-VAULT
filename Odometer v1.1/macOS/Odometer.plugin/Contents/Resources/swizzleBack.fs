#version 330
uniform sampler2D videoTexture;

in vec2 texCoord;
out vec4 colourOut;

void main() 
{
    colourOut = texture( videoTexture, texCoord );
    colourOut = colourOut.argb;
}
