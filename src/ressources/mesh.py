"""
mesh module
===========
Package: `ressources`

Module to/that # TODO: set docstring

Classes
-------
- `MeshParseData`
- `Mesh`
"""


# built-in imports
import os
import typing
import dataclasses
# pip imports
import pyglm.glm as glm
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, Ressource


@dataclasses.dataclass
class MeshParseData:
    """
    MeshParseData class
    ===================

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    positions: glm.array[GL.ctypes.c_float]
    texcoords: glm.array[GL.ctypes.c_float]
    normals: glm.array[GL.ctypes.c_float]
    nb: int

    def __post_init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        self.vertices: glm.array[GL.ctypes.c_float] = glm.array.zeros(self.nb * 24, GL.ctypes.c_float)
        self.indices: glm.array[GL.ctypes.c_uint32] = glm.array.zeros(self.nb * 3, GL.ctypes.c_uint32)
        self.index_map: dict[tuple[int, int, int], GL.ctypes.c_uint32] = {}
        self.current_index: int = 0
        self.parsed: int = 0


class Mesh(Ressource):
    """
    Mesh class
    ==========
    Parent class: `Ressource`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `__parseForArray` (staticmethod)
    - `__addToBuffers` (staticmethod)
    - `__parseForBuffers` (staticmethod)
    - `loadMesh` (staticmethod)
    """
    @staticmethod
    def __parseForArray(
            src: str,
            nb: int,
            pos: int,
            start: str,
            size: int,
            /
            ) -> glm.array[GL.ctypes.c_float]:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for mesh.
            nb (`int`): Number of element to parse.
            pos (`int`): Descriptor in the file.
            start (`str`): Start of lines to parse.
            size (`int`): Numbers of element to parse per line.
        Returns:
            `glm.array[GL.ctypes.c_float]`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        res: glm.array[GL.ctypes.c_float] = glm.array.zeros(nb * 3, GL.ctypes.c_float)

        parsed: int = 0
        min_len: int = len(start.strip()) + size * 2

        with open(src, "r") as file:
            file.seek(pos)

            for line in file:
                if parsed >= nb:
                    break
                if len(line) < min_len or not line.startswith(start):
                    continue

                res[parsed * size:parsed * size + size] = glm.array(list(map(GL.ctypes.c_float, map(float, line[len(start):].split(maxsplit=size)[:size]))))

                parsed += 1

        return res

    @staticmethod
    def __addToBuffers(
            data: MeshParseData,
            vertices: tuple[str, str, str],
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            data (`MeshParseData`): Data for mesh.
            vertices (`tuple[str, str, str]`): Vertices of the face.
        Raises:
            # TODO: set exceptions
        """
        for i, part in enumerate(vertices):
            pos_idx, tex_idx, norm_idx = [int(idx) - 1 for idx in part.split('/', 3)[:3]]
            key = (pos_idx, tex_idx, norm_idx)

            if key not in data.index_map:
                data.index_map[key] = GL.ctypes.c_uint32(data.current_index)
                data.vertices[data.current_index * 8:data.current_index * 8 + 8] = glm.array(
                    list(map(GL.ctypes.c_float, [
                        *data.positions[pos_idx * 3:pos_idx * 3 + 3],
                        *data.texcoords[tex_idx * 2:tex_idx * 2 + 2],
                        *data.normals[norm_idx * 3:norm_idx * 3 + 3],
                    ]))
                )
                data.current_index += 1

            data.indices[data.parsed * 3 + i] = data.index_map[key]

        data.parsed += 1

    @staticmethod
    def __parseForBuffers(
            src: str,
            pos: int,
            data: MeshParseData,
            /
            ) -> tuple[glm.array[GL.ctypes.c_float], glm.array[GL.ctypes.c_uint32]]:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for mesh.
            pos (`int`): Descriptor in the file.
            data (`MeshParseData`): Data for mesh.
        Returns:
            `tuple[glm.array[GL.ctypes.c_float],glm.array[GL.ctypes.c_uint32]]`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        with open(src, 'r') as file:
            file.seek(pos)

            for line in file:
                if data.parsed >= data.nb:
                    break
                if len(line) < 19 or line[0] != 'f' or line[1] != ' ':
                    continue

                parts = list(filter(lambda x: x.count('/') == 2, line[2:].split()[:4]))

                if len(parts) < 3:
                    continue

                Mesh.__addToBuffers(data, (parts[0], parts[1], parts[2]))

                if len(parts) == 4:
                    Mesh.__addToBuffers(data, (parts[0], parts[3], parts[2]))

        return data.vertices[0:data.current_index * 8], data.indices

    @staticmethod
    def loadMesh(
            src: str,
            /
            ) -> tuple[glm.array[GL.ctypes.c_float], glm.array[GL.ctypes.c_uint32]]:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for mesh.
        Returns:
            `tuple[glm.array[GL.ctypes.c_float],glm.array[GL.ctypes.c_uint32]]`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        nb_v = nb_vt = nb_vn = nb_f = 0
        pos_v = pos_vt = pos_vn = pos_f = -1

        min_len_v: int = 7
        min_len_vt: int = 6
        min_len_vn: int = 8
        min_len_f: int = 19

        with open(src, 'r') as file:
            while True:
                pos = file.tell()
                line = file.readline()

                if not line:
                    break

                if len(line) >= min_len_v and line.startswith("v "):
                    if not nb_v:
                        pos_v = pos
                    nb_v += 1
                elif len(line) >= min_len_vt and line.startswith("vt "):
                    if not nb_vt:
                        pos_vt = pos
                    nb_vt += 1
                elif len(line) >= min_len_vn and line.startswith("vn "):
                    if not nb_vn:
                        pos_vn = pos
                    nb_vn += 1
                elif len(line) >= min_len_f and line.startswith("f "):
                    if not nb_f:
                        pos_f = pos
                    nb_f += len(list(filter(lambda x: x.count('/') == 2, line[2:].split()[:4]))) - 2

        data: MeshParseData = MeshParseData(
            positions=Mesh.__parseForArray(src, nb_v, pos_v, "v ", 3),
            texcoords=Mesh.__parseForArray(src, nb_vt, pos_vt, "vt ", 2),
            normals=Mesh.__parseForArray(src, nb_vn, pos_vn, "vn ", 3),
            nb=nb_f
        )

        return Mesh.__parseForBuffers(src, pos_f, data)

    def __init__(
            self: typing.Self,
            mesh_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
        Raises:
            # TODO: set exceptions
        """
        super().__init__(mesh_name=mesh_name)

        self.vertices, self.indices = self.__class__.loadMesh(os.path.join(utils.ABS_PATH.meshes, mesh_name + utils.EXTENSIONS.mesh))

        self.vao: typing.Any = GL.glGenVertexArrays(1)
        self.vbo: typing.Any = GL.glGenBuffers(1)
        self.ibo: typing.Any = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.vao)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices.ptr, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices.ptr, GL.GL_STATIC_DRAW)

        type_bytes: int = GL.ctypes.sizeof(GL.ctypes.c_float)
        stride: int = 8 * type_bytes
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(3 * type_bytes))
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(5 * type_bytes))
        GL.glEnableVertexAttribArray(2)

        GL.glBindVertexArray(0)

    def clean(
            self: typing.Self,
            /
            ) -> int:
        """
        Method to/that # TODO: set docstring

        Returns:
            `int`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        if super().clean():
            return 1

        GL.glDeleteVertexArrays(1, (self.vao,))
        GL.glDeleteBuffers(2, (self.vbo, self.ibo))
        del self.indices
        del self.vertices

        return 0
