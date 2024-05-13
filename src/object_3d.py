import glm

from model_3d import Model3D


class Object3D:
    """Stores a Model3D and provides transformation and draw methods."""

    def __init__(self, model_path: str):
        self.transform = glm.mat4()
        self.model: Model3D = Model3D(model_path)

    def scale(self, axis: glm.vec3):
        self.transform = glm.scale(self.transform, axis)

    def rotate(self, angle: float, axis: glm.vec3):
        self.transform = glm.rotate(self.transform, angle, axis)

    def translate(self, axis: glm.vec3):
        self.transform = glm.translate(self.transform, axis)
