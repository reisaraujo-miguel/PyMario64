import math
from time import sleep

import glfw
import glm
import OpenGL.GL as gl

from camera import Camera
from object_3d import Object3D

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


def move_mario(
    window: glfw._GLFWwindow,
    mario: Object3D,
    speed: float,
    delta_time: float,
) -> None:
    if (glfw.get_key(window, glfw.KEY_W)) == glfw.PRESS:
        if mario.position.z < 90:
            mario.translate(glm.vec3(0, 0, speed), delta_time)

    elif (glfw.get_key(window, glfw.KEY_S)) == glfw.PRESS:
        if mario.position.z > -60:
            mario.translate(glm.vec3(0, 0, -speed), delta_time)

    elif (glfw.get_key(window, glfw.KEY_A)) == glfw.PRESS:
        if mario.position.x < 60:
            mario.translate(glm.vec3(speed, 0, 0), delta_time)

    elif (glfw.get_key(window, glfw.KEY_D)) == glfw.PRESS:
        if mario.position.x > -60:
            mario.translate(glm.vec3(-speed, 0, 0), delta_time)


def transform_mario(window, mario, delta_time):
    sleep(0.01)
    if glfw.get_key(window, glfw.KEY_E) == glfw.PRESS:
        mario.rotate(math.radians(180 * delta_time), glm.vec3(0, 1, 0))
    elif glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
        mario.rotate(-math.radians(180 * delta_time), glm.vec3(0, 1, 0))
    elif glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS:
        mario.scale(1, delta_time)
    elif glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS:
        mario.scale(-1, delta_time)


def rotate_camera(
    window: glfw._GLFWwindow,
    camera: Camera,
    sensitivity: float,
    delta_time: float,
) -> None:
    global last_x, last_y

    x_pos, y_pos = glfw.get_cursor_pos(window)

    yaw_offset: float = (x_pos - last_x) * sensitivity * delta_time
    pitch_offset: float = (y_pos - last_y) * sensitivity * delta_time

    camera.yaw += yaw_offset
    camera.yaw = camera.yaw % 360.0

    camera.pitch += pitch_offset
    camera.pitch = max(-50.0, min(camera.pitch, 4.0))

    if camera.target is not None:
        radius = glm.vec3(0.0, 1, 8)

        radius = glm.rotate(
            radius, math.radians(camera.pitch), glm.vec3(1, 0, 0)
        )

        radius = glm.rotate(
            radius, math.radians(camera.yaw + 90), glm.vec3(0, -1, 0)
        )

        camera.pos = camera.target.position + radius

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
