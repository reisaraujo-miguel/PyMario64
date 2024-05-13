import glfw
import OpenGL.GL as gl

import shaders


def create_window(height: int, width: int) -> glfw._GLFWwindow:
    """Initialise a hidden window and make it the current context."""
    glfw.init()
    glfw.window_hint(glfw.FOCUSED, glfw.FALSE)
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    glfw.window_hint(glfw.FOCUS_ON_SHOW, glfw.TRUE)
    window: glfw._GLFWwindow = glfw.create_window(
        height, width, "PyMario64", None, None
    )

    glfw.make_context_current(window)

    return window


def init_shaders(
    vertex_path: str, fragment_path: str
) -> tuple[None, None, None]:
    """Load and compile the shaders and link the program."""
    vertex, fragment = shaders.get_shaders(vertex_path, fragment_path)

    shaders.compile_shader(vertex)
    shaders.compile_shader(fragment)

    program: None = gl.glCreateProgram()

    gl.glAttachShader(program, vertex)
    gl.glAttachShader(program, fragment)

    shaders.link_program(program)

    gl.glUseProgram(program)

    return vertex, fragment, program
