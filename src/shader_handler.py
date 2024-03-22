import OpenGL.GL.shaders
from OpenGL.GL import *


def get_shaders():
    vertex_code = """
		attribute vec2 position;
		uniform mat4 mat_transformation;
		void main() {
			gl_Position = mat_transformation * vec4(position,0.0,1.0);
		}
		"""
    fragment_code = """
		void main() {
			gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
		}
		"""

    vertex = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    return vertex, fragment


def compile_shader(shader):
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        print(glGetShaderInfoLog(shader).decode())
        raise RuntimeError("Error compiling shader!")


def link_program(program):
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program).decode())
        raise RuntimeError('Error linking program')


def send_to_gpu(vertices, program):
    buffer = glGenBuffers(1)

    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
