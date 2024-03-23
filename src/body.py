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

        self.pos_x = 0.0
        self.pos_y = 0.0

        self.scale_x = 1.0
        self.scale_y = 1.0

        self.rotation = 0.0

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
