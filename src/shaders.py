import OpenGL.GL as gl

import util


def get_shaders(vertex_file: str, fragment_file: str) -> tuple[None, None]:
    """Create and source the shaders objects."""
    abs_vertex_path = util.get_path(vertex_file)
    abs_fragment_path = util.get_path(fragment_file)

    # check if it is possible to open the shader files
    try:
        with open(abs_vertex_path, "r") as file:
            vertex_code: str = file.read()
    except IOError as e:
        print(f"I't wasn't possible to open: \"{abs_vertex_path}\"\n{e}\n")
        raise RuntimeError("Error opening file!")

    try:
        with open(abs_fragment_path, "r") as file:
            fragment_code: str = file.read()
    except IOError as e:
        print(f"I't wasn't possible to open: \"{abs_fragment_path}\"\n{e}\n")
        raise RuntimeError("Error opening file!")

    vertex: None = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    fragment: None = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

    gl.glShaderSource(vertex, vertex_code)
    gl.glShaderSource(fragment, fragment_code)

    return vertex, fragment


def compile_shader(shader: None):
    """Compile a shader object."""
    gl.glCompileShader(shader)

    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        print(gl.glGetShaderInfoLog(shader).decode())
        raise RuntimeError("Error compiling shader!")


def link_program(program: None):
    "Link a program."
    gl.glLinkProgram(program)

    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        print(gl.glGetProgramInfoLog(program).decode())
        raise RuntimeError("Error linking program")
