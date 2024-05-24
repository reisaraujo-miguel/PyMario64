import math

import glfw
import glm

from camera import Camera
from object_3d import Object3D

last_x: float
last_y: float

toggle_flag: bool = False


def move_mario(
    window: glfw._GLFWwindow,
    mario: Object3D,
    speed: float,
    delta_time: float,
) -> None:
    try:
        assert mario.camera
    except AssertionError as e:
        print('The player instance must have a "Camera" object!\n')
        raise e

    movement_vector: glm.vec3 = glm.vec3()
    angle: float = 0
    qt_btn_pressed: int = 0

    if (glfw.get_key(window, glfw.KEY_W)) == glfw.PRESS:
        if mario.position.z < 90:
            movement_vector += glm.vec3(0, 0, 1)
            qt_btn_pressed += 1

    elif (glfw.get_key(window, glfw.KEY_S)) == glfw.PRESS:
        if mario.position.z > -60:
            movement_vector += glm.vec3(0, 0, -1)
            angle = glm.radians(-180)
            qt_btn_pressed += 1

    if (glfw.get_key(window, glfw.KEY_A)) == glfw.PRESS:
        if mario.position.x < 60:
            movement_vector += glm.vec3(1, 0, 0)
            qt_btn_pressed += 1
            angle = (abs(angle) + glm.radians(90)) / qt_btn_pressed

    elif (glfw.get_key(window, glfw.KEY_D)) == glfw.PRESS:
        if mario.position.x > -60:
            movement_vector += glm.vec3(-1, 0, 0)
            qt_btn_pressed += 1
            angle = (angle + glm.radians(-90)) / qt_btn_pressed

    movement_vector = glm.normalize(movement_vector)
    angle += glm.radians(90)

    if qt_btn_pressed > 0:
        mario.translate(movement_vector * speed, delta_time)
        mario.set_rotation(-mario.camera.yaw + angle, glm.vec3(0, 1, 0))

    mario.camera.pos = mario.position + mario.camera.radius


def transform_mario(window, mario, delta_time):
    if glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS:
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

    yaw_offset: float = (last_x - x_pos) * sensitivity * delta_time
    pitch_offset: float = (y_pos - last_y) * sensitivity * delta_time

    camera.yaw += yaw_offset
    camera.yaw = camera.yaw % glm.radians(360.0)

    camera.pitch += pitch_offset
    camera.pitch = max(glm.radians(-50.0), min(camera.pitch, glm.radians(4.0)))

    camera.radius = camera.distance_to_center

    camera.radius = glm.rotate(camera.radius, camera.pitch, glm.vec3(0, 0, 1))

    camera.radius = glm.rotate(camera.radius, -camera.yaw, glm.vec3(0, 1, 0))

    camera.front.x = math.cos(camera.yaw) * math.cos(camera.pitch)
    camera.front.y = math.sin(camera.pitch)
    camera.front.z = math.sin(camera.yaw) * math.cos(camera.pitch)
    camera.front = glm.normalize(camera.front)

    last_x = x_pos
    last_y = y_pos


def polygonal_mode(window: glfw._GLFWwindow, camera: Camera) -> None:
    global toggle_flag

    # This ensures the mode is toggled only after the key is released,
    # avoiding toggling it on and off when the key is held down.
    if glfw.get_key(window, glfw.KEY_P) == glfw.PRESS:
        toggle_flag = True

    elif toggle_flag is True:
        camera.toggle_polygonal_mode()
        toggle_flag = False


def window_focus(
    window: glfw._GLFWwindow,
) -> None:
    global last_x, last_y
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)
        last_x, last_y = glfw.get_cursor_pos(window)

    elif glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
