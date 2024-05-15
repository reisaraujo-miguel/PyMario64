import math
from time import sleep

import glfw
import glm
import OpenGL.GL as gl

from camera import Camera

last_x: float
last_y: float


def move_camera_pos(
    window: glfw._GLFWwindow,
    camera: Camera,
    camera_speed: float,
    delta_time: float,
) -> None:
    if (
        glfw.get_key(window, glfw.KEY_UP) or glfw.get_key(window, glfw.KEY_W)
    ) == glfw.PRESS:
        camera.pos += camera_speed * camera.front * delta_time

    elif (
        glfw.get_key(window, glfw.KEY_DOWN) or glfw.get_key(window, glfw.KEY_S)
    ) == glfw.PRESS:
        camera.pos -= camera_speed * camera.front * delta_time

    elif (
        glfw.get_key(window, glfw.KEY_LEFT) or glfw.get_key(window, glfw.KEY_A)
    ) == glfw.PRESS:
        camera.pos -= (
            glm.normalize(glm.cross(camera.front, camera.up))
            * camera_speed
            * delta_time
        )

    elif (
        glfw.get_key(window, glfw.KEY_RIGHT)
        or glfw.get_key(window, glfw.KEY_D)
    ) == glfw.PRESS:
        camera.pos += (
            glm.normalize(glm.cross(camera.front, camera.up))
            * camera_speed
            * delta_time
        )


def rotate_camera_view(
    window: glfw._GLFWwindow,
    camera: Camera,
    sensitivity: float,
    delta_time: float,
) -> None:
    global last_x, last_y

    x_pos, y_pos = glfw.get_cursor_pos(window)

    x_offset: float = (x_pos - last_x) * sensitivity * delta_time
    y_offset: float = (last_y - y_pos) * sensitivity * delta_time

    camera.yaw += x_offset
    camera.yaw = camera.yaw % 360.0

    camera.pitch += y_offset
    camera.pitch = max(-80.0, min(camera.pitch, 80.0))

    camera.front.x = math.cos(glm.radians(camera.yaw)) * math.cos(
        glm.radians(camera.pitch)
    )
    camera.front.y = math.sin(glm.radians(camera.pitch))
    camera.front.z = math.sin(glm.radians(camera.yaw)) * math.cos(
        glm.radians(camera.pitch)
    )
    camera.front = glm.normalize(camera.front)

    last_x = x_pos
    last_y = y_pos


def polygonal_mode(window: glfw._GLFWwindow, camera: Camera) -> None:
    polygonal_mode: bool = camera.polygonal_mode

    if polygonal_mode is True:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    if polygonal_mode is False:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
        camera.toggle_polygonal_mode()
        sleep(0.08)


def window_focus(
    window: glfw._GLFWwindow,
) -> None:
    global last_x, last_y
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        last_x, last_y = glfw.get_cursor_pos(window)

    elif glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
