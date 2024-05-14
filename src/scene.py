from pathlib import Path

import numpy as np
import OpenGL.GL as gl
from PIL import Image

from object_3d import Object3D


class Scene:
    """Handles storing and drawing objects."""

    def __init__(self, qt_textures: int) -> None:
        self.texture_coord_list: list = []
        self.last_texture_id: int = -1
        self.texture_dict: dict = {}

        self.vertices_list: list = []

        self.object_list: list[Object3D] = []

        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glEnable(gl.GL_TEXTURE_2D)

        self.textures = gl.glGenTextures(qt_textures)

    def load_scene(self, program: None) -> None:
        """Upload scene vertices and textures to the GPU."""
        self.upload_vertices(program)
        self.upload_textures(program)

    def add_object_to_scene(self, obj: Object3D) -> None:
        """Add object to the list of scene objects."""
        self.object_list.append(obj)

        for name, path in obj.texture_dict.items():
            if path is not None:
                self.load_texture(path, obj.texture_wrap)
                self.texture_dict[name] = self.last_texture_id
            else:
                self.texture_dict[name] = None

        self.vertices_list += obj.mesh_vertice_list
        self.texture_coord_list += obj.mesh_texture_coord_list

    def load_texture(self, path: Path, texture_wrap: int):
        """Read an image file and create a texture."""
        self.last_texture_id += 1

        wrap_mode = None

        match texture_wrap:
            case 0:
                wrap_mode = gl.GL_CLAMP_TO_EDGE
            case 1:
                wrap_mode = gl.GL_REPEAT

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.last_texture_id)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, wrap_mode)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, wrap_mode)

        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR
        )
        gl.glTexParameteri(
            gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR
        )

        img = Image.open(path)

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

    def upload_vertices(self, program: None) -> None:
        """Upload the global vertice list to the GPU."""
        buffer = gl.glGenBuffers(1)

        # uploading vertices
        np_vertices_list = np.zeros(
            len(self.vertices_list), [("position", np.float32, 3)]
        )
        np_vertices_list["position"] = self.vertices_list

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            np_vertices_list.nbytes,
            np_vertices_list,
            gl.GL_STATIC_DRAW,
        )

        stride = np_vertices_list.strides[0]
        offset = gl.ctypes.c_void_p(0)

        loc_vertices = gl.glGetAttribLocation(program, "position")
        gl.glEnableVertexAttribArray(loc_vertices)
        gl.glVertexAttribPointer(
            loc_vertices, 3, gl.GL_FLOAT, False, stride, offset
        )

    def upload_textures(self, program: None) -> None:
        """Upload the global texture coordinates list to the GPU."""

        buffer = gl.glGenBuffers(1)
        # uploading textures
        np_texture_coord_list = np.zeros(
            len(self.texture_coord_list), [("position", np.float32, 2)]
        )
        np_texture_coord_list["position"] = self.texture_coord_list

        # Upload data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            np_texture_coord_list.nbytes,
            np_texture_coord_list,
            gl.GL_STATIC_DRAW,
        )

        stride = np_texture_coord_list.strides[0]
        offset = gl.ctypes.c_void_p(0)

        loc_texture_coord = gl.glGetAttribLocation(program, "texture_coord")
        gl.glEnableVertexAttribArray(loc_texture_coord)
        gl.glVertexAttribPointer(
            loc_texture_coord, 2, gl.GL_FLOAT, False, stride, offset
        )

    def draw(self, program: None):
        """Draw every object in the scene."""
        loc_model = gl.glGetUniformLocation(program, "model")

        vertice_offset = 0

        for obj in self.object_list:
            gl.glUniformMatrix4fv(
                loc_model, 1, gl.GL_TRUE, np.array(obj.transform)
            )

            for mesh in obj.mesh_list:
                for i in range(mesh["mesh_size"]):
                    if self.texture_dict[mesh["mt_name"][i]] is not None:
                        gl.glBindTexture(
                            gl.GL_TEXTURE_2D,
                            self.texture_dict[mesh["mt_name"][i]],
                        )
                    else:
                        gl.glBindTexture(
                            gl.GL_TEXTURE_2D,
                            0,
                        )

                    gl.glDrawArrays(
                        gl.GL_TRIANGLES,
                        mesh["mt_start"][i] + vertice_offset,
                        mesh["mt_size"][i],
                    )

            vertice_offset += obj.model_size
