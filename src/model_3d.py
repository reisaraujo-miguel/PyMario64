from pathlib import Path

import util


class Model3D:
    """An Object that stores one or more 3D meshes"""

    def __init__(self, model_path: str, texture_wrap: int = 0) -> None:
        self.mesh_vertice_list: list = []
        self.mesh_texture_coord_list: list = []
        self.model_size: int = 0
        self.texture_dict: dict = {}
        self.mesh_list: list = []
        self.mtl: dict | None = None

        self.texture_wrap: int = texture_wrap

        self.load_model(model_path)

    def load_model(self, path: str) -> None:
        """Read a .obj save each object to the mesh list."""
        obj_vertices_list: list = []
        obj_texture_coord_list: list = []

        save_curr_object: bool = False

        mt_start_list: list = []  # list of the first vertice of each material
        mt_size_list: list = []  # amount of vertices of each material
        mt_name_list: list = []

        abs_path: Path = util.get_path(path)

        for line in open(abs_path, "r"):
            values = line.split()

            if line.startswith("#") or not values:
                continue  # ignore comments and blank lines

            match values[0]:
                case "mtllib":
                    mtl_path: Path = abs_path.parent / values[1]
                    self.load_mtl(mtl_path)

                case "o":  # reading an object inside the obj file
                    if save_curr_object:
                        mt_size_list.append(
                            (len(self.mesh_vertice_list) - mt_start_list[-1])
                        )

                        self.mesh_list.append(
                            self.create_mesh(
                                mt_start_list,
                                mt_size_list,
                                mt_name_list,
                            )
                        )

                    mt_start_list = []
                    mt_size_list = []
                    mt_name_list = []
                    save_curr_object = True

                case "v":
                    obj_vertices_list.append(values[1:4])

                case "vt":
                    obj_texture_coord_list.append(values[1:3])

                case "usemtl" | "usemat":
                    if len(mt_start_list) > 0:
                        # if this is not the first material we are reading,
                        # we need to save the size of the previous material
                        # before proceeding
                        mt_size_list.append(
                            (len(self.mesh_vertice_list) - mt_start_list[-1])
                        )

                    mt_start_list.append(len(self.mesh_vertice_list))
                    mt_name_list.append(values[1])

                case "f":
                    for face_vertice in values[1:]:
                        vertice_data = face_vertice.split("/")

                        self.mesh_vertice_list.append(
                            obj_vertices_list[int(vertice_data[0]) - 1]
                        )

                        if len(vertice_data) >= 2 and len(vertice_data[1]) > 0:
                            self.mesh_texture_coord_list.append(
                                obj_texture_coord_list[
                                    int(vertice_data[1]) - 1
                                ]
                            )
                        else:
                            self.mesh_texture_coord_list.append(["0.0", "0.0"])

        mt_size_list.append((len(self.mesh_vertice_list) - mt_start_list[-1]))

        self.mesh_list.append(
            self.create_mesh(
                mt_start_list,
                mt_size_list,
                mt_name_list,
            )
        )

        self.model_size = len(self.mesh_vertice_list)

    def create_mesh(
        self,
        mt_start_list,
        mt_size_list,
        mt_name_list,
    ):
        """Create a dict for the mesh."""
        object_dict = {
            "mt_start": mt_start_list,
            "mt_size": mt_size_list,
            "mt_name": mt_name_list,
            "mesh_size": len(mt_name_list),
        }

        return object_dict

    def load_mtl(self, path: str | Path):
        """Create a dict with each material name and it's texture id."""
        if isinstance(path, str):
            abs_path = util.get_path(path)
        else:
            abs_path = path

        filename: str = ""
        texture_name: str = ""

        is_prev_mapped: bool = True
        for line in open(abs_path, "r"):
            values = line.split()

            if line.startswith("#") or not values:
                continue  # ignore comments and blank lines

            elif values[0] == "newmtl":
                if not is_prev_mapped:
                    self.texture_dict[texture_name] = None

                texture_name = values[1]
                is_prev_mapped = False

            elif values[0] == "map_Kd":
                filename = values[1]
                self.texture_dict[texture_name] = abs_path.parent / filename
                is_prev_mapped = True
