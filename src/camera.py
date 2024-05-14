import glfw
import glm
import numpy as np
import OpenGL.GL as gl


class Camera:

    def __init__(self, window: glfw._GLFWwindow) -> None:
        self.pos: glm.vec3 = glm.vec3()
        self.front: glm.vec3 = glm.vec3()
        self.up: glm.vec3 = glm.vec3()

        self.mat_view: glm.mat4x4 = glm.mat4()
        self.mat_projection: glm.mat4x4 = glm.mat4()

        self.screen_width: float = glfw.get_window_size(window)[0]
        self.screen_height: float = glfw.get_window_size(window)[1]

        self.polygonal_mode: bool = False

    def update_view(self, program: None) -> None:
        self.mat_view: glm.mat4x4 = glm.lookAt(
            self.pos,
            self.pos + self.front,
            self.up,
        )

        loc_view = gl.glGetUniformLocation(program, "view")
        gl.glUniformMatrix4fv(loc_view, 1, gl.GL_TRUE, np.array(self.mat_view))

    def update_projection(self, program: None) -> None:
        self.mat_projection = glm.perspective(
            glm.radians(45.0),
            self.screen_width / self.screen_height,
            0.1,
            1000.0,
        )

        loc_projection = gl.glGetUniformLocation(program, "projection")
        gl.glUniformMatrix4fv(
            loc_projection, 1, gl.GL_TRUE, np.array(self.mat_projection)
        )

    def get_polygonal_mode(self) -> bool:
        return self.polygonal_mode

    def toggle_polygonal_mode(self) -> None:
        self.polygonal_mode = not self.polygonal_mode
