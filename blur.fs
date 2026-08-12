#version 330 core

in vec2 texCoord;
out vec4 FragColor;

uniform sampler2D videoTexture;
uniform float stride;
uniform int steps;

void main()
{
    if(steps == 0)
    {
        FragColor = texture(videoTexture, texCoord.xy);
    }
    else
    {
        int STEPS = steps;
        vec4 totalA = vec4(0.0);
        vec4 totalWeight = vec4(0.0);
        float weight = 2.0 / float(STEPS);
        
        for(int i = -STEPS; i <= STEPS; i++)
        {
            vec2 texCoord = texCoord.xy + vec2(0.0, float(i) * stride);
            totalA += vec4(weight) * texture(videoTexture, texCoord.xy);
            totalWeight += vec4(weight);
        }
        
        FragColor = totalA / totalWeight;
    }

    //FragColor = texture(inTex, texCoord.xy);
    //FragColor = vec4(0.5);
}
