#version 330

in vec4 vertex;
in vec2 tex;
uniform mat4 bufferResizeMat;

out vec2 texCoord;

void main()
{
    gl_Position = vertex * bufferResizeMat;
    texCoord = tex ;
}
