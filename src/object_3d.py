import glm

from model_3d import Model3D


class Object3D(Model3D):
    """Inherits from Model3D and provides transformation methods."""

    def __init__(self, model_path: str, texture_wrap: int = 0):
        self.transform = glm.mat4()
        super().__init__(model_path, texture_wrap)
        self.pos: glm.vec3 = glm.vec3()
        self.angle: glm.vec3 = glm.vec3()

    def scale(self, size: glm.vec3):
        self.transform = glm.scale(self.transform, size)

    def rotate(self, angle: float, axis: glm.vec3, delta_time=1.0):
        self.transform = glm.rotate(self.transform, angle * delta_time, axis)
        if axis.x != 0:
            self.angle.x = angle * delta_time

        if axis.y != 0:
            self.angle.y = angle * delta_time
        if axis.z != 0:
            self.angle.z = angle * delta_time

    def translate(self, pos: glm.vec3, delta_time=1.0):
        self.pos.x += pos.x * delta_time
        self.pos.y += pos.y * delta_time
        self.pos.z += pos.z * delta_time
        self.transform = glm.translate(self.transform, pos)
