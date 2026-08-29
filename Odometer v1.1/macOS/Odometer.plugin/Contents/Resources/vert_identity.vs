#version 330

in vec4 vertex;
in vec2 tex;

out vec2 texCoord;

void main() 
{
    gl_Position = vertex;
    texCoord = tex ;
}
