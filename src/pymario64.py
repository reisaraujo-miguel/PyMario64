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

BG_RED: float = 0.5
BG_BLUE: float = 0.5
BG_GREEN: float = 0.5
BG_ALPHA: float = 1.0

window: glfw._GLFWwindow = setup.create_window(480, 640)
vertex, fragment, program = setup.init_shaders(
    "./shaders/vertex.glsl", "./shaders/fragment.glsl"
)

camera: Camera = Camera(window)
camera.front = glm.vec3(0.0, 0.0, -50.0)
camera.pos = glm.vec3(0.0, 0.0, 50.0)
camera.up = glm.vec3(0.0, 50.0, 0.0)

main_scene: Scene = Scene(200, camera)

world: Object3D = Object3D("../assets/world/world.obj", 1)
world.translate(glm.vec3(0, -6, 0))
world.scale(glm.vec3(10.0, 10.0, 10.0))
main_scene.add_object_to_scene(world)

mario: Object3D = Object3D("../assets/mario/mario64.obj")
mario.scale(glm.vec3(0.01, 0.01, 0.01))
mario.translate(glm.vec3(0, -210, 0))
main_scene.add_object_to_scene(mario)

peach: Object3D = Object3D("../assets/peach/peach.obj")
peach.scale(glm.vec3(0.01, 0.01, 0.01))
peach.translate(glm.vec3(0, 260, 5900))
peach.rotate(glm.radians(180), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(peach)

yoshi: Object3D = Object3D("../assets/yoshi/yoshi.obj")
yoshi.scale(glm.vec3(0.4, 0.4, 0.4))
yoshi.translate(glm.vec3(-20, -3.7, 110))
yoshi.rotate(glm.radians(45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(yoshi)

toad: Object3D = Object3D("../assets/toad/toad.obj")
toad.scale(glm.vec3(0.01, 0.01, 0.01))
toad.translate(glm.vec3(800, -245, 5000))
toad.rotate(glm.radians(-45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(toad)

goomba: Object3D = Object3D("../assets/goomba/goomba.obj")
goomba.scale(glm.vec3(0.03, 0.03, 0.03))
goomba.translate(glm.vec3(-1300, -200, 130))
goomba.rotate(glm.radians(45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(goomba)

star: Object3D = Object3D("../assets/star/star.obj")
star.scale(glm.vec3(0.35, 0.35, 0.35))
star.translate(glm.vec3(100, -15, -15))
star.rotate(glm.radians(45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(star)

skybox: Object3D = Object3D("../assets/skybox/skybox.obj", 1)
main_scene.add_skybox_to_scene(skybox)

main_scene.load_scene(program)

camera_speed: float = 0.2
mouse_sensitivity: float = 0.1

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
gl.glEnable(gl.GL_DEPTH_TEST)

glfw.show_window(window)

delta_time: float = 0.0
last_frame: float = glfw.get_time()

while not glfw.window_should_close(window):
    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    input.window_lost_focus(window)
    input.check_polygonal_mode(window, camera)
    input.move_camera_pos(window, camera, camera_speed)
    input.rotate_camera_view(window, camera, mouse_sensitivity)

    main_scene.draw_scene(program)

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
