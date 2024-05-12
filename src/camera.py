import glm

polygonal_mode: bool = False


def view(
    camera_pos: glm.vec3, camera_front: glm.vec3, camera_up: glm.vec3
) -> glm.mat4x4:
    mat_view: glm.mat4x4 = glm.lookAt(
        camera_pos, camera_pos + camera_front, camera_up
    )

    return mat_view


def projection(
    mat_projection: glm.mat4x4,
    height: int,
    width: int,
) -> glm.mat4x4:
    mat_projection = glm.perspective(
        glm.radians(45.0), width / height, 0.1, 1000.0
    )

    return mat_projection


def get_polygonal_mode() -> bool:
    global polygonal_mode
    return polygonal_mode


def toggle_polygonal_mode() -> None:
    global polygonal_mode
    polygonal_mode = not polygonal_mode
