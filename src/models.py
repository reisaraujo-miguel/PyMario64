from pathlib import Path

import numpy as np
import OpenGL.GL as gl
from PIL import Image

import util

texture_id: int = 0
vertices_list: list = []
textures_coord_list: list = []


def read_obj(path: str) -> list:
    # Loads a Wavefront OBJ file and returns a list fo dictionaries
    vertices: list = []
    texture_coords: list = []
    faces: list = []
    mtl: dict | None = None

    material: str = ""
    obj_list: list = []
    obj_name: str = ""

    abs_path: Path = util.get_path(path)

    for line in open(abs_path, "r"):
        values = line.split()

        if line.startswith("#") or not values:
            continue  # ignore comments and blank lines

        match values[0]:
            case "mtllib":
                mtl_path: Path = abs_path.parent / values[1]
                print(f"mtl_path = {mtl_path}")
                mtl = read_mtl(mtl_path)

            case "o":  # reading an object inside the obj file
                if len(faces) > 0:
                    # after we read all the object data, we use this data to
                    # generate the object dict we will use to draw the object
                    print(20 * "#", obj_name, 20 * "#")
                    obj_list.append(
                        load_obj(
                            vertices,
                            texture_coords,
                            faces,
                            mtl,
                        )
                    )
                    faces = []

                obj_name = values[1]
                print(f"new obj: {obj_name}")

            case "v":
                vertices.append(values[1:4])

            case "vt":
                texture_coords.append(values[1:3])

            case "usemtl" | "usemat":
                material = values[1]  # get material name

            case "f":
                face_vertices = []
                face_texture_coords = []

                for vertice in values[1:]:
                    face_data = vertice.split("/")
                    face_vertices.append(int(face_data[0]))

                    if len(face_data) >= 2 and len(face_data[1]) > 0:
                        face_texture_coords.append(int(face_data[1]))
                    else:
                        face_texture_coords.append(0)

                faces.append((face_vertices, face_texture_coords, material))

    print(20 * "%", obj_name, 20 * "%")
    obj_list.append(
        load_obj(
            vertices,
            texture_coords,
            faces,
            mtl,
        )
    )

    return obj_list


def load_obj(
    vertices: list, texture_coords: list, faces: list, mtl: dict | None
) -> dict:
    global vertices_list
    global textures_coord_list

    face_start_list: list = []
    face_size_list: list = []  # amount of vertices in a face
    face_texture_list: list = []
    face_name_list: list = []
    faces_visited: list = []

    for face in faces:
        if face[2] not in faces_visited:
            if len(face_start_list) > 0:
                face_size_list.append(
                    (len(vertices_list) - face_start_list[-1])
                )
                print(
                    faces_visited[-1],
                    "face size:",
                    face_size_list[-1],
                    "\n",
                )

            print(face[2], "vertice inicial:", len(vertices_list))
            face_start_list.append(len(vertices_list))

            if mtl is not None:
                face_texture_list.append(mtl[face[2]])
                print(f"appended {mtl[face[2]]} to face_texture")
            else:
                face_texture_list.append(None)
                print("appended 'None' to face_texture")

            faces_visited.append(face[2])
            face_name_list.append(face[2])

        for vertice_id in face[0]:
            vertices_list.append(vertices[vertice_id - 1])

        for texture_id in face[1]:
            textures_coord_list.append(texture_coords[texture_id - 1])

    if len(face_start_list) > 0:
        face_size_list.append(len(vertices_list) - face_start_list[-1])
        print(faces_visited[-1], "face size:", face_size_list[-1], "\n")

    model_dict = {
        "face_start": face_start_list,
        "face_size": face_size_list,
        "face_texture": face_texture_list,
        "face_name": face_name_list,
        "model_size": len(faces_visited),
        "mtl_dict": mtl,
    }

    return model_dict


def read_mtl(path: str | Path) -> dict | None:
    global texture_id

    if isinstance(path, str):
        abs_path = util.get_path(path)
    else:
        abs_path = path

    mtl: dict = {}

    mtl_material_name: str = ""
    mtl_filename: str = ""

    print(f"reading mtl: {abs_path}\n")
    for line in open(abs_path, "r"):
        values = line.split()

        if line.startswith("#") or not values:
            continue  # ignore comments and blank lines

        elif values[0] == "newmtl":
            mtl_material_name = values[1]
            print(f"new material name: {mtl_material_name}")

        elif values[0] == "map_Kd":
            mtl_filename = values[1]
            mtl_material_id: int = read_texture(abs_path.parent / mtl_filename)

            print(
                f"name: {mtl_material_name}, file: {mtl_filename}, "
                f"id: {mtl_material_id}\n"
            )

            mtl[mtl_material_name] = mtl_material_id

    if mtl:
        return mtl
    else:
        return None


def read_texture(path: str | Path) -> int:
    global texture_id

    if isinstance(path, str):
        abs_path = util.get_path(path)
    else:
        abs_path = path

    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)

    print(f"file {abs_path} bind to id {texture_id}")

    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE
    )

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
