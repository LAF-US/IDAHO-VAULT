#version 330
uniform sampler2D videoTexture;
uniform float uvScaleY; // account for user defined height of the geo
uniform float uvOffsetY; // initially to make sure 0 stays in the middle regardless of the user defined height

uniform float xOffsetStartF;
uniform float xOffsetEndF;
uniform float uvScaleX; // 1.0 for numbers, but separators are user defined

uniform float numCharsF;

uniform float debug_left;

in vec2 texCoord;
out vec4 colourOut;

void main()
{
    vec2 texSize = textureSize(videoTexture, 0);
    
    float aspectY = texSize.x / texSize.y;

    vec2 uvMod = vec2(texCoord.x, texCoord.y * aspectY * uvScaleY);
    
    uvMod.y += (uvScaleY - 1.0) * (-0.5 * (1.0 / numCharsF)); // wtf lol
    uvMod.y += uvOffsetY - floor(uvOffsetY);

    colourOut = texture( videoTexture, uvMod );
    
    //colourOut = texture( videoTexture, texCoord ); // debug, original coords
}
