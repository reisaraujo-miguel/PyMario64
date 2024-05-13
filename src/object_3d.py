import glm

from model_3d import Model3D


class Object3D(Model3D):
    """Inherits from Model3D and provides transformation methods."""

    def __init__(self, model_path: str, texture_wrap: int = 0):
        self.transform = glm.mat4()
        super().__init__(model_path, texture_wrap)

    def scale(self, axis: glm.vec3):
        self.transform = glm.scale(self.transform, axis)

    def rotate(self, angle: float, axis: glm.vec3):
        self.transform = glm.rotate(self.transform, angle, axis)

    def translate(self, axis: glm.vec3):
        self.transform = glm.translate(self.transform, axis)
