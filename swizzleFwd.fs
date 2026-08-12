#version 330
uniform sampler2D videoTexture;

in vec2 texCoord;
out vec4 colourOut;

uniform float bgOpacityF;
uniform vec3 bgColorF;

void main()
{
    colourOut = texture(videoTexture, texCoord);
    colourOut = colourOut.gbar;
    colourOut.rgb *= vec3(colourOut.a);
    
    if(bgOpacityF > 0.0)
    {
        float weightF = 1.0 - colourOut.a;
        colourOut.a += weightF * bgOpacityF;
        colourOut.rgb += vec3(weightF * bgColorF * bgOpacityF);
        colourOut.rgb = min(colourOut.rgb, 1.0);
    }
}
