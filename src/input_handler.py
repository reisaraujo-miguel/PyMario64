import glfw
import numpy as np


def check_movement(window, speed, factor):
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        speed += factor
    elif glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        speed -= factor

    return speed


def check_scale(window, x, y, factor):
    if glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS:
        x += factor
        y += factor
    elif glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS and x > 0 < y:
        x -= factor
        y -= factor

    return x, y


def check_rotation(window, x, y, angle):
    width, height = glfw.get_framebuffer_size(window)

    origin_x, origin_y = width / 2, height / 2
    cursor_x, cursor_y = glfw.get_cursor_pos(window)

    cat_x = (cursor_x - origin_x) - (x * origin_x)
    cat_y = (origin_y - cursor_y) - (y * origin_y)

    if cat_y > 0:
        angle = np.arctan(cat_x / cat_y)
    elif cat_x > 0:
        angle = np.arctan(-cat_y / cat_x) + 1.571
    else:
        angle = np.arctan(-cat_y / cat_x) - 1.571

    return angle
