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
        print("#" * 20, "drawing", "#" * 20)
        loc_model = gl.glGetUniformLocation(program, "model")

        gl.glUniformMatrix4fv(
            loc_model, 1, gl.GL_TRUE, np.array(self.transform)
        )

        for model in self.model_list:
            for i in range(model["model_size"]):
                if model["face_texture"][i] is not None:
                    gl.glBindTexture(
                        gl.GL_TEXTURE_2D, model["face_texture"][i]
                    )
                    print(f"texture id: {model["face_texture"][i]} "
                          f"texture name: {model["face_name"][i]}")

                print(f"start: {model["face_start"][i]}, "
                      f"size: {model["face_size"][i]}\n")

                gl.glDrawArrays(
                    gl.GL_TRIANGLES,
                    model["face_start"][i],
                    model["face_size"][i],
                )

    def scale(self, x: float, y: float, z: float):
        self.transform = glm.scale(self.transform, glm.vec3(x, y, z))

    def rotate(self, angle: float, x: float, y: float, z: float):
        self.transform = glm.rotate(self.transform, angle, glm.vec3(x, y, z))

    def translate(self, x: float, y: float, z: float):
        self.transform = glm.translate(self.transform, glm.vec3(x, y, z))
