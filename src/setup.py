import glfw
import OpenGL.GL as gl

import shaders


def create_window(height: int, width: int) -> glfw._GLFWwindow:
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window: glfw._GLFWwindow = glfw.create_window(
        height, width, "PyMario64", None, None
    )

    glfw.make_context_current(window)

    return window


def init_shaders() -> tuple[None, None, None]:
    vertex, fragment = shaders.get_shaders(
        "./shaders/vertex.glsl", "./shaders/fragment.glsl"
    )

    shaders.compile_shader(vertex)
    shaders.compile_shader(fragment)

    program: None = gl.glCreateProgram()

    gl.glAttachShader(program, vertex)
    gl.glAttachShader(program, fragment)

    shaders.link_program(program)

    gl.glUseProgram(program)

    return vertex, fragment, program


def init_textures(qt: int) -> None:
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glEnable(gl.GL_LINE_SMOOTH)
    gl.glEnable(gl.GL_TEXTURE_2D)
    textures = gl.glGenTextures(qt)

    return textures
