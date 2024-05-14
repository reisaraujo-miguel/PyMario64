import os

# OpenGl doesn't work well on wayland, so it's better to use XWayland
if os.environ["XDG_SESSION_TYPE"] == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"


import glfw
import glm
import OpenGL.GL as gl

import input
import setup
from camera import Camera
from object_3d import Object3D
from scene import Scene

height: float = 600
width: float = 600

window: glfw._GLFWwindow = setup.create_window(height, width)
vertex, fragment, program = setup.init_shaders(
    "./shaders/vertex.glsl", "./shaders/fragment.glsl"
)

main_scene: Scene = Scene(200)

world: Object3D = Object3D("../assets/world/world.obj", 1)
world.translate(glm.vec3(0, -6, 0))
world.scale(glm.vec3(10.0, 10.0, 10.0))
main_scene.add_object_to_scene(world)

mario: Object3D = Object3D("../assets/mario/mario64.obj", 0)
mario.scale(glm.vec3(0.01, 0.01, 0.01))
mario.translate(glm.vec3(0, -210, 0))
main_scene.add_object_to_scene(mario)

main_scene.load_scene(program)

camera: Camera = Camera(window)

BG_RED: float = 0.5
BG_BLUE: float = 0.5
BG_GREEN: float = 0.5
BG_ALPHA: float = 1.0

angle: float = 0.0
translation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0)
delta_time: float = 0.0
last_frame: float = glfw.get_time()

camera_speed: float = 0.2
mouse_sensitivity: float = 0.2

yaw: float = -90.0
pitch: float = 0.0
last_x, last_y = glfw.get_cursor_pos(window)

glfw.set_window_focus_callback(window, input.window_focus_callback)
glfw.show_window(window)
glfw.set_cursor_pos(window, last_x, last_y)
gl.glEnable(gl.GL_DEPTH_TEST)

while not glfw.window_should_close(window):
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    if input.window_lost_focus(window):
        last_x, last_y = glfw.get_cursor_pos(window)

    input.move_camera_pos(window, camera, camera_speed)

    last_x, last_y, yaw, pitch = input.rotate_camera_view(
        window, camera, last_x, last_y, yaw, pitch, mouse_sensitivity
    )

    input.check_polygonal_mode(window, camera)

    camera.update_view(program)
    camera.update_projection(program)

    main_scene.draw(program)

    glfw.poll_events()
    glfw.swap_buffers(window)
    # break


glfw.terminate()
