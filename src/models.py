import numpy as np
import OpenGL.GL as gl
from PIL import Image

import util

texture_id = 0
vertices_list = []
textures_coord_list = []


def read_obj(path: str) -> dict:
    """Loads a Wavefront OBJ file."""
    vertices = []
    texture_coords = []
    faces = []
    material = ""

    abs_path = util.get_path(path)

    for line in open(abs_path, "r"):
        values = line.split()

        if line.startswith("#") or not values:
            continue  # ignore comments and blank lines

        match values[0]:
            case "v":
                vertices.append(values[1:4])

            case "vt":
                texture_coords.append(values[1:3])

            case "usemtl" | "usemat":
                material = values[1]

            case "f":
                face = []
                face_texture = []

                for v in values[1:]:
                    w = v.split("/")
                    face.append(int(w[0]))

                    if len(w) >= 2 and len(w[1]) > 0:
                        face_texture.append(int(w[1]))
                    else:
                        face_texture.append(0)

                faces.append((face, face_texture, material))

    obj_file = {
        "vertices": vertices,
        "texture": texture_coords,
        "faces": faces,
    }

    return obj_file


def read_mtl(path: str) -> dict:
    global texture_id

    abs_path = util.get_path(path)

    for line in open(abs_path, "r"):
        values = line.split()

        if line.startswith("#") or not values:
            continue  # ignore comments and blank lines

        match values[0]:
            case "newmtl":
                pass

    a = {}

    return a


def read_texture(path: str) -> int:
    global texture_id

    abs_path = util.get_path(path)

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR
    )

    img = Image.open(abs_path)

    img_width = img.size[0]
    img_height = img.size[1]

    image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)

    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA,
        img_width,
        img_height,
        0,
        gl.GL_RGBA,
        gl.GL_UNSIGNED_BYTE,
        image_data,
    )

    texture_id += 1

    return texture_id - 1


def load_model(model: dict) -> dict:
    global vertices_list
    global textures_coord_list

    face_start_list: list = []
    face_size_list: list = []  # amount of vertices in a face
    face_texture_list: list = []

    for face in model["faces"]:
        print(face[2], " vertice inicial =", len(vertices_list))
        face_start_list.append(len(vertices_list))
        face_texture_list.append(face[2])

        for vertice_id in face[0]:
            vertices_list.append(model["vertices"][vertice_id - 1])

        for texture_id in face[1]:
            textures_coord_list.append(model["texture"][texture_id - 1])

        face_size_list.append(len(vertices_list))

    model_dict = {
        "face_start": face_start_list,
        "face_size": face_size_list,
        "face_texture": face_texture_list,
    }

    return model_dict


def upload_vertices(program: None):
    global vertices_list
    buffer = gl.glGenBuffers(1)

    # uploading vertices
    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices["position"] = vertices_list

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW
    )

    stride = vertices.strides[0]
    offset = gl.ctypes.c_void_p(0)

    loc_vertices = gl.glGetAttribLocation(program, "position")
    gl.glEnableVertexAttribArray(loc_vertices)
    gl.glVertexAttribPointer(
        loc_vertices, 3, gl.GL_FLOAT, False, stride, offset
    )


def upload_textures(program: None):
    global textures_coord_list

    buffer = gl.glGenBuffers(1)
    # uploading textures
    textures = np.zeros(
        len(textures_coord_list), [("position", np.float32, 2)]
    )
    textures["position"] = textures_coord_list

    # Upload data
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER, textures.nbytes, textures, gl.GL_STATIC_DRAW
    )

    stride = textures.strides[0]
    offset = gl.ctypes.c_void_p(0)

    loc_texture_coord = gl.glGetAttribLocation(program, "texture_coord")
    gl.glEnableVertexAttribArray(loc_texture_coord)
    gl.glVertexAttribPointer(
        loc_texture_coord, 2, gl.GL_FLOAT, False, stride, offset
    )
