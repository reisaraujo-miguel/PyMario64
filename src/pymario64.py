import os

# OpenGl doesn't work well on wayland, so it's better to use XWayland
if os.environ["XDG_SESSION_TYPE"] == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"


import glfw
import glm
import numpy as np
import OpenGL.GL as gl

import camera
import input
import models
import setup
from body import Body

height: float = 600
width: float = 600

window: glfw._GLFWwindow = setup.create_window(height, width)
vertex, fragment, program = setup.init_shaders()
textures: None = setup.init_textures(100)

mario: Body = Body()
mario.add_model("../assets/mario/mario64.obj")
mario.scale(glm.vec3(0.05, 0.05, 0.05))

models.upload_vertices(program)
models.upload_textures(program)

BG_RED: float = 0.5
BG_BLUE: float = 0.5
BG_GREEN: float = 0.5
BG_ALPHA: float = 1.0

angle: float = 0.0
translation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
camera_speed: float = 0.4
delta_time: float = 0.0
last_frame: float = glfw.get_time()

camera_pos: glm.vec3 = glm.vec3(0.0, 0.0, 50.0)
camera_front: glm.vec3 = glm.vec3(0.0, 0.0, -50.0)
camera_up: glm.vec3 = glm.vec3(0.0, 50.0, 0.0)
mouse_sensitivity: float = 0.2

mat_projection: glm.mat4x4 = glm.mat4x4()
mat_view: glm.mat4x4 = glm.mat4x4()

yaw: float = -90.0
pitch: float = 0.0
last_x: float = width / 2
last_y: float = height / 2

glfw.show_window(window)
glfw.set_cursor_pos(window, last_x, last_y)

gl.glEnable(gl.GL_DEPTH_TEST)

while not glfw.window_should_close(window):
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    camera_pos = input.move_camera_pos(
        window, camera_pos, camera_front, camera_up, camera_speed
    )

    camera_front, last_x, last_y, yaw, pitch = input.move_camera_view(
        window, last_x, last_y, yaw, pitch, mouse_sensitivity
    )

    input.check_polygonal_mode(window)

    mat_view = camera.view(camera_pos, camera_front, camera_up)

    loc_view = gl.glGetUniformLocation(program, "view")
    gl.glUniformMatrix4fv(loc_view, 1, gl.GL_TRUE, np.array(mat_view))

    mat_projection = camera.projection(mat_projection, height, width)

    loc_projection = gl.glGetUniformLocation(program, "projection")
    gl.glUniformMatrix4fv(
        loc_projection, 1, gl.GL_TRUE, np.array(mat_projection)
    )

    mario.draw(program)

    glfw.poll_events()
    glfw.swap_buffers(window)


glfw.terminate()
