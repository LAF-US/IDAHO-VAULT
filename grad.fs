#version 330

uniform float xcoord;
uniform float ycoord;
uniform float heightRelF;
uniform float height;
uniform float scale;

out vec4 FragColour;
in vec2 texCoord;
                  
void main(void)
{
    float top = (ycoord * 0.5) - (heightRelF * height);
    float bot = (ycoord * 0.5) + (heightRelF * height);
    float multiplier = 1.0 / ((heightRelF * height));

    if(texCoord.y > top + (heightRelF * height))
    {
        FragColour.rgb = vec3((bot - texCoord.y) * multiplier);
    }
    else
    {
        FragColour.rgb = vec3((texCoord.y - top) * multiplier);
    }

    FragColour.rgb = max(FragColour.rgb, 0.0);
    FragColour.a = 1.0;

}
