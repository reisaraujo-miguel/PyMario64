import glfw
import numpy as np
import OpenGL.GL as gl

import shader_handler as shader
from body import Body

glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(600, 600, "PyMario64", None, None)

glfw.make_context_current(window)

vertex, fragment = shader.get_shaders()

shader.compile_shader(vertex)
shader.compile_shader(fragment)

program = gl.glCreateProgram()

gl.glAttachShader(program, vertex)
gl.glAttachShader(program, fragment)

shader.link_program(program)

gl.glUseProgram(program)

global_vertices = np.zeros(0, [("position", np.float32, 2)])

ship_vertices = np.zeros(3, [("position", np.float32, 2)])
ship_vertices["position"] = [
    (+0.00, +0.05),
    (+0.05, -0.05),
    (-0.05, -0.05),
]

box_vertices = np.zeros(4, [("position", np.float32, 2)])
box_vertices["position"] = [
    (+0.10, -0.05),
    (+0.10, +0.05),
    (+0.20, -0.05),
    (+0.20, +0.05),
]

ship = Body()
global_vertices = ship.instantiate(ship_vertices, global_vertices)

box = Body()
global_vertices = box.instantiate(box_vertices, global_vertices)

shader.send_to_gpu(global_vertices, program)

glfw.show_window(window)

BG_RED = 0.03
BG_BLUE = 0.03
BG_GREEN = 0.03
BG_ALPHA = 1.0

angle = 0.0
s_x, s_y = 1.0, 1.0
t_x, t_y = 0.0, 0.0
speed = 0.0
size_factor = 0.05
speed_factor = 0.05
delta_time = 0.0
last_frame = glfw.get_time()

while not glfw.window_should_close(window):
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    ship.draw(program)
    box.draw(program)

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
