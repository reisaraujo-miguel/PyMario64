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
camera.front = glm.vec3(0.0, 0.0, 0.0)
camera.pos = glm.vec3(0.0, 6, -15)
camera.up = glm.vec3(0.0, 50.0, 0.0)

camera.set_distance_to_center(glm.vec3(-8, 1, 0))

main_scene: Scene = Scene(200, camera)

world: Object3D = Object3D("../assets/world/world.obj", 1)
world.set_scale(glm.vec3(10.0, 10.0, 10.0))
main_scene.add_object_to_scene(world)

mario: Object3D = Object3D("../assets/mario/mario64.obj")
mario.set_pos(glm.vec3(0, 4, -10))
mario.set_scale(glm.vec3(0.01, 0.01, 0.01))
mario.camera = camera
camera.pos = mario.position + camera.radius
main_scene.add_object_to_scene(mario)

peach: Object3D = Object3D("../assets/peach/peach.obj")
peach.set_pos(glm.vec3(0, 8.5, 60))
peach.set_scale(glm.vec3(0.01, 0.01, 0.01))
peach.set_rotation(glm.radians(180), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(peach)

yoshi: Object3D = Object3D("../assets/yoshi/yoshi.obj")
yoshi.set_pos(glm.vec3(-9, 5, 45))
yoshi.set_scale(glm.vec3(0.4, 0.4, 0.4))
yoshi.set_rotation(glm.radians(45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(yoshi)

toad: Object3D = Object3D("../assets/toad/toad.obj")
toad.set_pos(glm.vec3(9, 3.8, 46))
toad.set_scale(glm.vec3(0.01, 0.01, 0.01))
toad.set_rotation(glm.radians(-45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(toad)

goomba: Object3D = Object3D("../assets/goomba/goomba.obj")
goomba.set_pos(glm.vec3(-40, 0, 4))
goomba.set_scale(glm.vec3(0.03, 0.03, 0.03))
goomba.set_rotation(glm.radians(45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(goomba)

star: Object3D = Object3D("../assets/star/star.obj")
star.set_pos(glm.vec3(46, -0.5, -14))
star.set_scale(glm.vec3(0.35, 0.35, 0.35))
star.set_rotation(glm.radians(-45), glm.vec3(0, 1, 0))
main_scene.add_object_to_scene(star)


skybox: Object3D = Object3D("../assets/skybox/skybox.obj", 1)
main_scene.add_skybox_to_scene(skybox)

main_scene.load_scene(program)

camera_speed: float = 15
mario_speed: float = 15
mouse_sensitivity: float = 0.1

gl.glEnable(gl.GL_DEPTH_TEST)
glfw.show_window(window)

delta_time: float = 0.0
last_frame: float = glfw.get_time()

while not glfw.window_should_close(window):
    glfw.poll_events()

    current_frame = glfw.get_time()
    delta_time = current_frame - last_frame
    last_frame = current_frame

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glClear(gl.GL_DEPTH_BUFFER_BIT)
    gl.glClearColor(BG_RED, BG_GREEN, BG_BLUE, BG_ALPHA)

    input.window_focus(window)
    input.polygonal_mode(window, camera)
    input.rotate_camera(window, camera, mouse_sensitivity, delta_time)
    input.move_mario(window, mario, mario_speed, delta_time)
    input.transform_mario(window, mario, delta_time)

    main_scene.draw_scene(program)

    glfw.swap_buffers(window)

glfw.terminate()
