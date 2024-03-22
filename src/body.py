import numpy as np
from OpenGL.GL import *


class Body:
    def __init__(self):
        self.rotation_mat = np.array([[1.0, 0.0, 0.0, 0.0],
                                      [0.0, 1.0, 0.0, 0.0],
                                      [0.0, 0.0, 1.0, 0.0],
                                      [0.0, 0.0, 0.0, 1.0]], np.float32)
        self.scale_mat = np.array([[1.0, 0.0, 0.0, 0.0],
                                   [0.0, 1.0, 0.0, 0.0],
                                   [0.0, 0.0, 1.0, 0.0],
                                   [0.0, 0.0, 0.0, 1.0]], np.float32)
        self.translation_mat = np.array([[1.0, 0.0, 0.0, 0.0],
                                         [0.0, 1.0, 0.0, 0.0],
                                         [0.0, 0.0, 1.0, 0.0],
                                         [0.0, 0.0, 0.0, 1.0]], np.float32)

        self.pos_x = 0.0
        self.pos_y = 0.0

        self.scale_x = 1.0
        self.scale_y = 1.0

        self.rotation = 0.0

        self.start_vertice = 0.0
        self.vertice_count = 0.0

    def instantiate(self, vertices, global_vertices):
        self.start_vertice = len(global_vertices)
        self.vertice_count = len(vertices)

        global_vertices = np.concatenate(
            (global_vertices, vertices))

        return global_vertices

    def draw_body(self, program):
        transformation_mat = self.translation_mat @ self.rotation_mat @ self.scale_mat

        loc = glGetUniformLocation(program, "mat_transformation")

        glUniformMatrix4fv(loc, 1, GL_TRUE, transformation_mat)

        glDrawArrays(GL_TRIANGLE_STRIP, self.start_vertice, self.vertice_count)
