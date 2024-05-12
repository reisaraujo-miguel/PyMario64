import glm
import numpy as np
import OpenGL.GL as gl

import models


class Body:
    def __init__(self):
        self.transform = glm.mat4(1.0)

        self.model_list: list = []

    def add_model(self, model_path: str):
        obj_list: list = models.read_obj(model_path)

        for obj in obj_list:
            self.model_list.append(obj)

    def draw(self, program: None):
        loc_model = gl.glGetUniformLocation(program, "model")

        gl.glUniformMatrix4fv(
            loc_model, 1, gl.GL_TRUE, np.array(self.transform)
        )

        for model in self.model_list:
            for i in range(model["model_size"]):
                if model["material_texture"][i] is not None:
                    gl.glBindTexture(
                        gl.GL_TEXTURE_2D, model["material_texture"][i]
                    )

                gl.glDrawArrays(
                    gl.GL_TRIANGLES,
                    model["material_start"][i],
                    model["material_size"][i],
                )

    def scale(self, axis: glm.vec3):
        self.transform = glm.scale(self.transform, axis)

    def rotate(self, angle: float, axis: glm.vec3):
        self.transform = glm.rotate(self.transform, angle, axis)

    def translate(self, axis: glm.vec3):
        self.transform = glm.translate(self.transform, axis)
