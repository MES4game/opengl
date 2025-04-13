# -*- coding: utf-8 -*-
"""
mesh module
===========
This module contains the `Mesh` class, which is used to load and compile meshes for OpenGL rendering.\n

It creates the `Mesh` class as a subclass of `Ressource`, which is a base class for all resources in the application.\n

The `Mesh` class has methods to load mesh data from a file, create vertex and index buffers, and clean up resources when the object is deleted.
"""


# built-in imports
import os
import typing
# pip imports
import numpy
import numpy.typing as tnumpy
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, Ressource


class LineInfo:
    """
    This class is used to store the information of a line in a mesh file.
    The `add` method is used to add a new line to the linked list, and the `aft` attribute is used to point to the next line.
    The `values` attribute is used to store the values of the line.\n
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initialize the `LineInfo` object.\n

        The `aft` attribute is set to `self`, and the `values` attribute is set to `None`.
        """
        self.aft = self
        self.values = None

    def add(
            self: typing.Self,
            values: tnumpy.NDArray[numpy.single],
            /
            ) -> typing.Self:
        """
        Add a new line to the linked list.\n

        The `values` attribute is set to the values passed as an argument, and the `aft` attribute is set a new line that we create.\n

        Parameters:
            values (tnumpy.NDArray[numpy.single]): The values to add to the linked list.

        Returns:
            typing.Self: The next line in the linked list that has been created.
        """
        self.values = values
        self.aft: typing.Self = self.__class__()

        return self.aft


class Mesh(Ressource):
    """
    Parent class: `Ressource`\n

    Class to load a mesh for OpenGL.\n

    If you instantiate the class with a mesh name, it will load the mesh from the file and create the vertex array and vertex/index buffers.
    If you instantiate the class with `mesh_name=""`, it will create empty buffers.\n

    When the object is deleted, it will delete the vertex array and vertex/index buffers.\n
    """
    @classmethod
    def loadMesh(
            cls: type[typing.Self],
            mesh_name: str,
            /
            ) -> tuple[tnumpy.NDArray[numpy.single], tnumpy.NDArray[numpy.uint32]]:
        """
        Load a mesh from a file.\n

        This method reads the mesh file and extracts the vertex, texture coordinate, normal and face data.
        It also returns them as vertex and index arrays.\n

        Here is the format of the mesh file:
        - Lines starting with `v` are vertex positions (3 floats): v x y z.
        - Lines starting with `vt` are texture coordinates (2 floats): vt u v.
        - Lines starting with `vn` are vertex normals (3 floats): vn nx ny nz.
        - Lines starting with `f` are faces (3 vertex indices, starting at 1 and not 0): f v1/vt1/vn1 v2/vt2/vn2 v3/vt3/vn3.\n

        Parameters:
            mesh_name (str): The name of the mesh file to load (without extension).

        Returns:
            tnumpy.NDArray[numpy.single],tnumpy.NDArray[numpy.uint32]: A tuple containing the vertex and index arrays.\n

            The vertex array contains the vertex positions, texture coordinates, and normals like that `(x, y, z, u, v, nx, ny, nz)`.
            The index array contains the indices of the vertices in the vertex array.
        """
        nb_v = nb_vt = nb_vn = nb_f = 0
        current_v: LineInfo = LineInfo()
        current_vt: LineInfo = LineInfo()
        current_vn: LineInfo = LineInfo()

        lines_v: LineInfo = current_v
        lines_vt: LineInfo = current_vt
        lines_vn: LineInfo = current_vn

        with open(os.path.join(utils.ABS_PATH.meshes, mesh_name + utils.EXTENSIONS.mesh), 'r') as file:
            for line in file:
                if line.startswith("v "):
                    current_v = current_v.add(numpy.fromstring(line[2:], dtype=numpy.single, count=3, sep=' '))
                    nb_v += 1
                elif line.startswith("vt "):
                    current_vt = current_vt.add(numpy.fromstring(line[3:], dtype=numpy.single, count=2, sep=' '))
                    nb_vt += 1
                elif line.startswith("vn "):
                    current_vn = current_vn.add(numpy.fromstring(line[3:], dtype=numpy.single, count=3, sep=' '))
                    nb_vn += 1
                elif line.startswith("f "):
                    nb_f += len(line[2:].split()[:4]) - 2

        positions: tnumpy.NDArray[numpy.single] = numpy.empty((nb_v * 3,), dtype=numpy.single)
        for i in range(nb_v):
            if lines_v.values is None:
                break
            positions[i * 3:i * 3 + 3] = lines_v.values
            if lines_v.aft is lines_v:
                break
            lines_v = lines_v.aft
        del lines_v
        del current_v

        texcoords: tnumpy.NDArray[numpy.single] = numpy.empty((nb_vt * 2,), dtype=numpy.single)
        for i in range(nb_vt):
            if lines_vt.values is None:
                break
            texcoords[i * 2:i * 2 + 2] = lines_vt.values
            if lines_vt.aft is lines_vt:
                break
            lines_vt = lines_vt.aft
        del lines_vt
        del current_vt

        normals: tnumpy.NDArray[numpy.single] = numpy.empty((nb_vn * 3,), dtype=numpy.single)
        for i in range(nb_vn):
            if lines_vn.values is None:
                break
            normals[i * 3:i * 3 + 3] = lines_vn.values
            if lines_vn.aft is lines_vn:
                break
            lines_vn = lines_vn.aft
        del lines_vn
        del current_vn

        size1: int = nb_f * 3
        size2: int = size1 * 8
        parsed: int = 0

        current_index: numpy.uint32 = numpy.uint32(0)
        index_map: dict[tuple[int, int, int], numpy.uint32] = {}

        vertices: tnumpy.NDArray[numpy.single] = numpy.empty((size2,), dtype=numpy.single)
        indices: tnumpy.NDArray[numpy.uint32] = numpy.empty((size1,), dtype=numpy.uint32)

        with open(os.path.join(utils.ABS_PATH.meshes, mesh_name + utils.EXTENSIONS.mesh), 'r') as file:
            for line in file:
                if parsed >= nb_f:
                    break
                if len(line) < 19 or line[0] != 'f' or line[1] != ' ':
                    continue

                parts = line[2:].split()[:4]

                if len(parts) < 3:
                    continue

                if len(parts) == 4:
                    for i, part in enumerate((parts[0], parts[3], parts[2])):
                        pos_idx, tex_idx, norm_idx = [int(idx) - 1 for idx in part.split('/', 3)[:3]]
                        key = (pos_idx, tex_idx, norm_idx)

                        if key not in index_map:
                            index_map[key] = current_index
                            vertices[current_index * 8:current_index * 8 + 8] = numpy.array([
                                *positions[pos_idx * 3:pos_idx * 3 + 3],
                                *texcoords[tex_idx * 2:tex_idx * 2 + 2],
                                *normals[norm_idx * 3:norm_idx * 3 + 3],
                            ], dtype=numpy.single)
                            current_index += 1

                        indices[parsed * 3 + i] = index_map[key]
                    parsed += 1

                for i, part in enumerate((parts[0], parts[1], parts[2])):
                    pos_idx, tex_idx, norm_idx = [int(idx) - 1 for idx in part.split('/', 3)[:3]]
                    key = (pos_idx, tex_idx, norm_idx)

                    if key not in index_map:
                        index_map[key] = current_index
                        vertices[current_index * 8:current_index * 8 + 8] = numpy.array([
                            *positions[pos_idx * 3:pos_idx * 3 + 3],
                            *texcoords[tex_idx * 2:tex_idx * 2 + 2],
                            *normals[norm_idx * 3:norm_idx * 3 + 3],
                        ], dtype=numpy.single)
                        current_index += 1

                    indices[parsed * 3 + i] = index_map[key]

                parsed += 1

        return vertices[0:current_index * 8], indices

    def __init__(
            self: typing.Self,
            /,
            *,
            mesh_name: str = "",
            ) -> None:
        """
        Initialize the `Mesh` object.\n

        If the `mesh_name` is not empty, it will load the mesh from the file and create the vertex array and vertex/index buffers.
        If the `mesh_name` is empty, it will create empty buffers.\n

        Parameters:
            mesh_name (str): The name of the mesh file to load (without extension).
        """
        super().__init__(mesh_name=mesh_name)

        if mesh_name == "":
            self.vertices = numpy.empty((0,), dtype=numpy.single)
            self.indices = numpy.empty((0,), dtype=numpy.uint32)
        else:
            self.vertices, self.indices = self.__class__.loadMesh(mesh_name)

        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        self.ibo = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.vao)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL.GL_STATIC_DRAW)

        type_bytes = GL.ctypes.sizeof(GL.ctypes.c_float)
        stride = 8 * type_bytes
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(3 * type_bytes))
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, GL.ctypes.c_void_p(5 * type_bytes))
        GL.glEnableVertexAttribArray(2)

    def __del__(
            self: typing.Self,
            /
            ) -> None:
        """
        Delete the `Mesh` object.\n

        This method deletes the vertex array and vertex/index buffers.
        """
        super().__del__()

        GL.glDeleteVertexArrays(1, (self.vao,))
        GL.glDeleteBuffers(2, (self.vbo, self.ibo))
