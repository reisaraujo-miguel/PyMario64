import glm

from camera import Camera
from model_3d import Model3D


class Object3D(Model3D):
    """Inherits from Model3D and provides transformation methods."""

    def __init__(self, model_path: str, texture_wrap: int = 0) -> None:
        self.translation_mat: glm.mat4 = glm.mat4()
        self.scale_mat: glm.mat4 = glm.mat4()
        self.rotation_mat: glm.mat4 = glm.mat4()

        super().__init__(model_path, texture_wrap)

        self.position: glm.vec3 = glm.vec3()
        self.rotation: glm.vec3 = glm.vec3()
        self.size: glm.vec3 = glm.vec3()

        self.camera: Camera | None = None

    def scale(self, speed: float, delta_time=1.0) -> None:
        """
        Scale the object by the `speed`.

        `speed` defines the time (in seconds) it takes for the object to
        double in size.
        """
        scale: glm.vec3 = glm.vec3(glm.exp2(speed * delta_time))
        self.size *= scale
        self.scale_mat = glm.scale(self.scale_mat, scale)

    def set_scale(self, size: glm.vec3) -> None:
        self.size = size
        self.scale_mat = glm.scale(size)

    def rotate(self, angle: float, axis: glm.vec3, delta_time=1.0) -> None:
        """
        Rotate the object by the `angle` factor.

        `angle` defines the angle (in radians) the object will be rotated
        (relative to it's previous rotation) in one second.
        """
        self.rotation_mat = glm.rotate(
            self.rotation_mat, angle * delta_time, axis
        )
        self.rotation += axis * angle * delta_time

    def set_rotation(self, angle: float, axis: glm.vec3) -> None:
        self.rotation_mat = glm.rotate(angle, axis)
        self.rotation = axis * angle

    def translate(self, speed: glm.vec3, delta_time=1.0):
        """
        Translate the object by the `speed` factor.

        `speed` defines the amount of pixels the object will be translated
        (relative to it's previous position) in one second.

        If there a camera was set, then the object axes will always be treated
        in relation to the camera view.
        """
        if self.camera is not None:
            speed = glm.rotate(
                speed, -self.camera.yaw + glm.radians(90), glm.vec3(0, 1, 0)
            )

            self.camera.pos = self.position + self.camera.radius

        self.translation_mat = glm.translate(
            self.translation_mat, speed * delta_time
        )
        self.position += speed * delta_time

    def set_pos(self, pos: glm.vec3) -> None:
        self.position = pos
        self.translation_mat = glm.translate(pos)

    def get_transformation(self) -> glm.mat4x4:
        transform_mat: glm.mat4 = (
            self.translation_mat @ self.rotation_mat @ self.scale_mat
        )

        return transform_mat
