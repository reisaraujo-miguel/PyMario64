import os

# OpenGl doesn't work well on wayland, so it's better to use XWayland
if os.environ["XDG_SESSION_TYPE"] == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"


import math

import glfw
import glm
import numpy as np
import OpenGL.GL as gl

# import input_handler as inpt
import models
import setup
from body import Body

height = 600
width = 600

window = setup.create_window(height, width)
vertex, fragment, program = setup.init_shaders()
textures = setup.init_textures(100)

monstro = Body()
monstro.add_model("../assets/monstro/monstro.obj")

models.upload_vertices(program)
models.upload_textures(program)

BG_RED = 1.0
BG_BLUE = 1.0
BG_GREEN = 1.0
BG_ALPHA = 1.0

angle = 0.0
s_x, s_y = 1.0, 1.0
t_x, t_y = 0.0, 0.0
speed = 0.0
size_factor = 0.05
speed_factor = 0.05
delta_time = 0.0
last_frame = glfw.get_time()

camera_pos = glm.vec3(0.0, 0.0, 1.0)
camera_front = glm.vec3(0.0, 0.0, -1.0)
camera_up = glm.vec3(0.0, 1.0, 0.0)

inc_fov = 0
inc_near = 0
inc_far = 0
inc_view_up = 0


def view():
    global camera_pos, camera_front, camera_up
    mat_view = glm.lookAt(camera_pos, camera_pos + camera_front, camera_up)
    mat_view = np.array(mat_view)
    return mat_view


def projection():
    global height, width, inc_fov, inc_near, inc_far
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(
        glm.radians(45.0), width / height, 0.1, 1000.0
    )
    mat_projection = np.array(mat_projection)
    return mat_projection


polygonal_mode = False


def key_event(key, action):
    global camera_pos, camera_front, camera_up, polygonal_mode
    global inc_fov, inc_near, inc_far, inc_view_up
    camera_speed = 0.2

    if key == 66:
        inc_view_up += 0.1

    if key == 78:
        inc_near += 0.1

    if key == 77:
        inc_far -= 5

    if key == 87 and (action == 1 or action == 2):  # tecla W
        camera_pos += camera_speed * camera_front

    if key == 83 and (action == 1 or action == 2):  # tecla S
        camera_pos -= camera_speed * camera_front

    if key == 65 and (action == 1 or action == 2):  # tecla A
        camera_pos -= (
            glm.normalize(glm.cross(camera_front, camera_up)) * camera_speed
        )

    if key == 68 and (action == 1 or action == 2):  # tecla D
        camera_pos += (
            glm.normalize(glm.cross(camera_front, camera_up)) * camera_speed
        )

    if key == 80 and action == 1 and polygonal_mode is True:
        polygonal_mode = False
    else:
        if key == 80 and action == 1 and polygonal_mode is False:
            polygonal_mode = True


first_mouse = True
yaw = -90.0
pitch = 0.0
lastX = width / 2
lastY = height / 2


def mouse_event(window, xpos, ypos):
    global first_mouse, camera_front, yaw, pitch, lastX, lastY
    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.3
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset
    pitch += yoffset

    if pitch >= 90.0:
        pitch = 90.0
    if pitch <= -90.0:
        pitch = -90.0

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    camera_front = glm.normalize(front)


glfw.set_key_callback(window, key_event)
glfw.set_cursor_pos_callback(window, mouse_event)

glfw.show_window(window)
glfw.set_cursor_pos(window, lastX, lastY)

gl.glEnable(gl.GL_DEPTH_TEST)

while not glfw.window_should_close(window):
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    if polygonal_mode is True:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    if polygonal_mode is False:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    # s_x, s_y = inpt.check_scale(window, s_x, s_y, size_factor * delta_time)
    # ship.resize(s_x, s_y)

    # angle = inpt.check_rotation(window, t_x, t_y)
    # ship.rotate(angle)

    # speed = inpt.check_movement(window, speed, speed_factor)
    # t_x, t_y = ship.move_towards_mouse(window, t_x, t_y, speed * delta_time)
    # t_x, t_y = ship.screen_wrap(t_x, t_y)
    # ship.translate(t_x, t_y)

    # ship.draw(program)
    # box.draw(program)

    monstro.draw(program)

    mat_view = view()
    loc_view = gl.glGetUniformLocation(program, "view")
    gl.glUniformMatrix4fv(loc_view, 1, gl.GL_TRUE, mat_view)

    mat_projection = projection()
    loc_projection = gl.glGetUniformLocation(program, "projection")
    gl.glUniformMatrix4fv(loc_projection, 1, gl.GL_TRUE, mat_projection)

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
