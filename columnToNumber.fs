#version 330
uniform sampler2D videoTexture;
uniform float uvScaleY; // account for user defined height of the geo
uniform float uvOffsetY; // initially to make sure 0 stays in the middle regardless of the user defined height

uniform float xOffsetStartF;
uniform float widthF; // 1.0 for numbers, but separators are user defined

uniform float debug_left;

in vec2 texCoord;
out vec4 colourOut;

void main()
{
    vec2 uvMod = vec2(texCoord.x * 0.5 * widthF, texCoord.y * uvScaleY); // * 0.5 as we're using only half of the two column texture, either the numbers or the symbols
    
    uvMod.x += xOffsetStartF;
    
    uvMod.y -= uvScaleY * 0.5;
    uvMod.y += 0.05;
    uvMod.y += uvOffsetY - floor(uvOffsetY);

    colourOut = texture( videoTexture, uvMod );
    
    //colourOut = texture( videoTexture, texCoord ); // debug, original coords
}
