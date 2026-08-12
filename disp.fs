#version 330 core

in vec2 texCoord;
out vec4 FragColor;

uniform sampler2D videoTexture;
uniform sampler2D map;

uniform float perspF;
uniform float aspectF;

uniform float ycoord;
uniform float heightRelF;
uniform float height;
uniform float geoToOutputHeightRatioF;

uniform float scale; // if the geo is scaled. this used to be done on CPU

uniform int bicubicL; // if 1, just a single sample. if > 1, do bicubic fetch
uniform int previewFeatherL; // 1 if we want to view the feather map

//uniform float featherF; deprecated, just have featherRad
uniform float featherRadF;

vec2 modifyCoords(  float translateXF,
                    float translateYF,
                    float scaleXF,
                    float scaleYF)
{
    //vec2 aspectRatio = vec2((resV.y / resV.x), 1.0); // TODO: play with this, incorrect aspect ratio can create more interesting results!

    float anchorX = 0.0;
    float anchorY = (ycoord * 0.5);

    // position
    vec2 posCoords = texCoord;

    // scale
    vec2 scaleCoords = vec2(scaleXF, scaleYF) * (posCoords - vec2(anchorX, anchorY));
    scaleCoords += vec2(anchorX, anchorY);
    return scaleCoords;
}

void main()
{
    float featherMult = 0.0;
    float grey = 0.0;
    vec2 modUVs = texCoord;

    if(perspF > 0.0)
    {
        grey = texture(map, texCoord.xy).r;
        grey = mix(1.0, grey, perspF / scale); // account for amount of perspective
        modUVs = modifyCoords(0.0, 0.0, 1.0, 1.0 / grey);
    }

    FragColor = texture(videoTexture, modUVs);
    
    if(featherRadF > 0.0 || previewFeatherL > 0)
    {
        float heightPerspF = 0.0;
        float featherRadMod = (1.0 - featherRadF);// / scale;
        float dist = (ycoord * 0.5 * 1.0) - modUVs.y; // draw a grad
        float dist2 = (modUVs.y - (ycoord * 0.5 * 1.0));
        
        dist -= featherRadMod * (geoToOutputHeightRatioF * 0.5); // change anchor of grad to bounds of geo
        dist2 -= featherRadMod * (geoToOutputHeightRatioF * 0.5);

        dist = max(dist, dist2);
        
        dist /= scale; // account for previous cpu scale

        featherMult = dist;
        featherMult /= (geoToOutputHeightRatioF * 0.5) * (1.0 - featherRadMod);
        featherMult = min(featherMult, 1.0);
        featherMult = max(featherMult, 0.0);
        featherMult = 1.0 - featherMult;
        
        FragColor *= vec4(featherMult);

        if(previewFeatherL > 0)
        {
            FragColor = vec4(featherMult);
        }
        
        //FragColor = vec4(0.2);
    }

    //FragColor = texture(videoTexture, texCoord);
    //FragColor = vec4(0.5);
}
