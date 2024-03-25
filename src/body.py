import glfw
import numpy as np
import OpenGL.GL as gl


class Body:
    def __init__(self):
        self.rotation_mat = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )
        self.scale_mat = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )
        self.translat_mat = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )

        self.start_vert = 0.0
        self.vert_count = 0.0

    def instantiate(self, vertices, global_vertices):
        self.start_vert = len(global_vertices)
        self.vert_count = len(vertices)

        global_vertices = np.concatenate((global_vertices, vertices))

        return global_vertices

    def draw(self, program):
        transform_mat = self.translat_mat @ self.rotation_mat @ self.scale_mat

        loc = gl.glGetUniformLocation(program, "mat_transformation")

        gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, transform_mat)

        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, self.start_vert, self.vert_count)

    def resize(self, x, y):
        self.scale_mat = np.array(
            [
                [x, 0.0, 0.0, 0.0],
                [0.0, y, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )

    def rotate(self, angle):
        cos = np.cos(-angle)
        sin = np.sin(-angle)

        self.rotation_mat = np.array(
            [
                [cos, -sin, 0.0, 0.0],
                [sin, cos, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )

    def translate(self, x, y):
        self.translat_mat = np.array(
            [
                [1.0, 0.0, 0.0, x],
                [0.0, 1.0, 0.0, y],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ],
            np.float32,
        )

    def move_towards_mouse(self, window, x, y, factor):
        width, height = glfw.get_framebuffer_size(window)

        origin_x, origin_y = width / 2, height / 2
        cursor_x, cursor_y = glfw.get_cursor_pos(window)

        cat_x = (cursor_x - origin_x) - (x * origin_x)
        cat_y = (origin_y - cursor_y) - (y * origin_y)

        vector_magnitude = np.sqrt(pow(cat_x, 2) + pow(cat_y, 2))

        x_component = cat_x / vector_magnitude
        y_component = cat_y / vector_magnitude

        x += factor * x_component
        y += factor * y_component

        return x, y

    def screen_wrap(self, x, y):
        if x > 1:
            x = -1
        elif x < -1:
            x = 1

        if y > 1:
            y = -1
        elif y < -1:
            y = 1

        return x, y
