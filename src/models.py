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
    global vertices_list
    global textures_coord_list

    mtl: dict | None = None
    vertices: list = []
    texture_coords: list = []
    new_object: bool = False

    material: str = ""
    model_list: list = []
    material_start_list: list = []
    material_size_list: list = []  # amount of vertices with this material
    material_texture_list: list = []
    material_name_list: list = []

    abs_path: Path = util.get_path(path)

    for line in open(abs_path, "r"):
        values = line.split()

        if line.startswith("#") or not values:
            continue  # ignore comments and blank lines

        match values[0]:
            case "mtllib":
                mtl_path: Path = abs_path.parent / values[1]
                mtl = read_mtl(mtl_path)

            case "o":  # reading an object inside the obj file
                if new_object:
                    material_size_list.append(
                        (len(vertices_list) - material_start_list[-1])
                    )

                    model_list.append(
                        create_model(
                            material_start_list,
                            material_size_list,
                            material_texture_list,
                            material_name_list,
                            mtl,
                        )
                    )

                material_start_list: list = []
                material_size_list: list = []
                material_texture_list: list = []
                material_name_list: list = []

            case "v":
                vertices.append(values[1:4])

            case "vt":
                texture_coords.append(values[1:3])

            case "usemtl" | "usemat":
                if len(material_start_list) > 0:
                    # if this is not the first material we are reading,
                    # we need to save the size of the previous material
                    # before proceeding
                    material_size_list.append(
                        (len(vertices_list) - material_start_list[-1])
                    )

                material = values[1]

                material_start_list.append(len(vertices_list))

                if mtl is not None:
                    material_texture_list.append(mtl[material])
                else:
                    material_texture_list.append(None)

                material_name_list.append(material)

            case "f":
                for face_vertice in values[1:]:
                    vertice_data = face_vertice.split("/")
                    vertices_list.append(vertices[int(vertice_data[0]) - 1])

                    if len(vertice_data) >= 2 and len(vertice_data[1]) > 0:
                        textures_coord_list.append(
                            texture_coords[int(vertice_data[1]) - 1]
                        )

                    else:
                        textures_coord_list.append(0)

                new_object = True

    material_size_list.append((len(vertices_list) - material_start_list[-1]))

    model_list.append(
        create_model(
            material_start_list,
            material_size_list,
            material_texture_list,
            material_name_list,
            mtl,
        )
    )

    return model_list


def create_model(
    material_start_list,
    material_size_list,
    material_texture_list,
    material_name_list,
    mtl,
):
    model_dict = {
        "material_start": material_start_list,
        "material_size": material_size_list,
        "material_texture": material_texture_list,
        "material_name": material_name_list,
        "model_size": len(material_name_list),
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

        elif values[0] == "map_Kd":
            mtl_filename = values[1]
            mtl_material_id: int = read_texture(abs_path.parent / mtl_filename)
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
