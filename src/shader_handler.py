import OpenGL.GL as gl


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

    vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    gl.glShaderSource(vertex, vertex_code)
    gl.glShaderSource(fragment, fragment_code)

    return vertex, fragment


def compile_shader(shader):
    gl.glCompileShader(shader)

    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        print(gl.glGetShaderInfoLog(shader).decode())
        raise RuntimeError("Error compiling shader!")


def link_program(program):
    gl.glLinkProgram(program)

    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        print(gl.glGetProgramInfoLog(program).decode())
        raise RuntimeError("Error linking program")


def send_to_gpu(vert, program):
    buffer = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    gl.glBufferData(gl.GL_ARRAY_BUFFER, vert.nbytes, vert, gl.GL_DYNAMIC_DRAW)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

    stride = vert.strides[0]
    offset = gl.ctypes.c_void_p(0)

    loc = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc)
    gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)
