import glm
import numpy as np
import OpenGL.GL as gl

import models


class Body:
    def __init__(self):
        self.transform = glm.mat4(1.0)

        self.model: dict = {}

    def add_model(self, model_path: str):
        obj_file = models.read_obj(model_path)
        self.model = models.load_model(obj_file)

    def draw(self, program: None):
        loc_model = gl.glGetUniformLocation(program, "model")

        gl.glUniformMatrix4fv(
            loc_model, 1, gl.GL_TRUE, np.array(self.transform)
        )

        for i in range(len(self.model["face_start"])):
            # gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

            gl.glDrawArrays(
                gl.GL_TRIANGLES,
                self.model["face_start"][i],
                self.model["face_size"][i],
            )

    def scale(self, x: float, y: float, z: float):
        self.transform = glm.scale(self.transform, glm.vec3(x, y, z))

    def rotate(self, angle: float, x: float, y: float, z: float):
        self.transform = glm.rotate(self.transform, angle, glm.vec3(x, y, z))

    def translate(self, x: float, y: float, z: float):
        self.transform = glm.translate(self.transform, glm.vec3(x, y, z))
