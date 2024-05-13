import math

import glfw
import glm
import OpenGL.GL as gl

import camera


def move_camera_pos(
    window: glfw._GLFWwindow,
    camera_pos: glm.vec3,
    camera_front: glm.vec3,
    camera_up: glm.vec3,
    camera_speed: float,
) -> glm.vec3:
    if (
        glfw.get_key(window, glfw.KEY_UP) or glfw.get_key(window, glfw.KEY_W)
    ) == glfw.PRESS:
        camera_pos += camera_speed * camera_front

    elif (
        glfw.get_key(window, glfw.KEY_DOWN) or glfw.get_key(window, glfw.KEY_S)
    ) == glfw.PRESS:
        camera_pos -= camera_speed * camera_front

    elif (
        glfw.get_key(window, glfw.KEY_LEFT) or glfw.get_key(window, glfw.KEY_A)
    ) == glfw.PRESS:
        camera_pos -= (
            glm.normalize(glm.cross(camera_front, camera_up)) * camera_speed
        )

    elif (
        glfw.get_key(window, glfw.KEY_RIGHT)
        or glfw.get_key(window, glfw.KEY_D)
    ) == glfw.PRESS:
        camera_pos += (
            glm.normalize(glm.cross(camera_front, camera_up)) * camera_speed
        )

    return camera_pos


def move_camera_view(
    window: glfw._GLFWwindow,
    last_x: float,
    last_y: float,
    yaw: float,
    pitch: float,
    sensitivity: float,
) -> tuple[glm.vec3, float, float, float, float]:
    x_pos, y_pos = glfw.get_cursor_pos(window)

    x_offset: float = (x_pos - last_x) * sensitivity
    y_offset: float = (last_y - y_pos) * sensitivity

    yaw += x_offset
    pitch += y_offset

    if pitch >= 90.0:
        pitch = 90.0
    if pitch <= -90.0:
        pitch = -90.0

    camera_front = glm.vec3()
    camera_front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    camera_front.y = math.sin(glm.radians(pitch))
    camera_front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))

    last_x = x_pos
    last_y = y_pos

    return glm.normalize(camera_front), last_x, last_y, yaw, pitch


def check_polygonal_mode(window: glfw._GLFWwindow) -> None:
    if glfw.get_key(window, glfw.KEY_P):
        camera.toggle_polygonal_mode()

    polygonal_mode: bool = camera.get_polygonal_mode()

    if polygonal_mode is True:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    if polygonal_mode is False:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)


def window_focus_callback(window: glfw._GLFWwindow, focused: bool):
    if focused:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)


def window_lost_focus(
    window: glfw._GLFWwindow,
) -> bool:
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        return True

    elif glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    return False
