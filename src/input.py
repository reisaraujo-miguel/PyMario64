import math

import glfw
import glm
import OpenGL.GL as gl

from camera import Camera


def move_camera_pos(
    window: glfw._GLFWwindow,
    camera: Camera,
    camera_speed: float,
) -> None:
    if (
        glfw.get_key(window, glfw.KEY_UP) or glfw.get_key(window, glfw.KEY_W)
    ) == glfw.PRESS:
        camera.pos += camera_speed * camera.front

    elif (
        glfw.get_key(window, glfw.KEY_DOWN) or glfw.get_key(window, glfw.KEY_S)
    ) == glfw.PRESS:
        camera.pos -= camera_speed * camera.front

    elif (
        glfw.get_key(window, glfw.KEY_LEFT) or glfw.get_key(window, glfw.KEY_A)
    ) == glfw.PRESS:
        camera.pos -= (
            glm.normalize(glm.cross(camera.front, camera.up)) * camera_speed
        )

    elif (
        glfw.get_key(window, glfw.KEY_RIGHT)
        or glfw.get_key(window, glfw.KEY_D)
    ) == glfw.PRESS:
        camera.pos += (
            glm.normalize(glm.cross(camera.front, camera.up)) * camera_speed
        )


def rotate_camera_view(
    window: glfw._GLFWwindow,
    camera: Camera,
    last_x: float,
    last_y: float,
    yaw: float,
    pitch: float,
    sensitivity: float,
) -> tuple[float, float, float, float]:
    x_pos, y_pos = glfw.get_cursor_pos(window)

    x_offset: float = (x_pos - last_x) * sensitivity
    y_offset: float = (last_y - y_pos) * sensitivity

    yaw += x_offset
    pitch += y_offset

    if pitch >= 85.0:
        pitch = 85.0
    elif pitch <= -85.0:
        pitch = -85.0

    if yaw >= 360.0:
        yaw = -360.0
    elif yaw <= -360.0:
        yaw = 360.0

    camera.front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    camera.front.y = math.sin(glm.radians(pitch))
    camera.front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    camera.front = glm.normalize(camera.front)

    last_x = x_pos
    last_y = y_pos

    return last_x, last_y, yaw, pitch


def check_polygonal_mode(window: glfw._GLFWwindow, camera: Camera) -> None:
    if glfw.get_key(window, glfw.KEY_P):
        camera.toggle_polygonal_mode()

    polygonal_mode: bool = camera.get_polygonal_mode()

    if polygonal_mode is True:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    if polygonal_mode is False:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)


def window_lost_focus(
    window: glfw._GLFWwindow,
) -> bool:
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        return True

    elif glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    return False
