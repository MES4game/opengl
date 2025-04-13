# -*- coding: utf-8 -*-
"""
shape module
============
This module contains the `Shape` class, which is a base class for all elements to render in the scene.\n

It contains the methods to set the position, rotation and size of the shape, as well as the methods to render it.
"""


# built-in imports
import typing
# pip imports
import numpy
import pyrr  # type: ignore
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, ressources
if typing.TYPE_CHECKING:
    from . import Node


class Shape:
    """
    Class to represent a shape in the scene.\n

    It contains the methods to set the position, rotation and size of the shape, as well as the methods to render it.
    It also contains the methods to set the material and the texture of the shape.
    There is also a method to switch the light of the shape on and off.\n

    It is a base class for all elements to render in the scene.
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            parent: "Node | None" = None,
            shader_name: str = "",
            mesh_name: str = ""
            ) -> None:
        """
        Initialize the `Shape` object.\n

        This method initializes the position, rotation and size of the shape, as well as the shader and the mesh to use for rendering.
        It also initializes the material and the texture to None.\n

        Parameters:
            parent (Node | None): The parent of the shape. If None, the shape is not attached to any parent.
            shader_name (str): The name of the shader file (without extension) to use for rendering the shape.
            mesh_name (str): The name of the mesh file (without extension) to use for rendering the shape.
        """
        self.parent: Node | None = parent

        self.pos = pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single)
        self.rot = pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single)
        self.size = pyrr.Vector3([1.0, 1.0, 1.0], dtype=numpy.single)

        self.shader = ressources.Shader(shader_name=shader_name)
        self.mesh = ressources.Mesh(mesh_name=mesh_name)
        self.has_light = False
        self.material = None
        self.texture = None

        self.updateModelMatrix()

    def switchLight(
            self: typing.Self,
            /
            ) -> None:
        """
        Switch the light of the shape on and off.
        """
        self.has_light = not self.has_light

    def setMaterial(
            self: typing.Self,
            material_name: str,
            /
            ) -> None:
        """
        # TODO
        """
        if self.material is not None:
            del self.material
        # TODO
        self.material = ressources.Material()

    def setTexture(
            self: typing.Self,
            texture_name: str,
            /
            ) -> None:
        """
        # TODO
        """
        if self.texture is not None:
            del self.texture
        # TODO
        self.texture = ressources.Texture()

    def setCoord(
            self: typing.Self,
            /,
            *,
            pos: pyrr.Vector3 | None = None,
            rot: pyrr.Vector3 | None = None,
            size: pyrr.Vector3 | None = None
            ) -> None:
        """
        Set the position, rotation and/or size of the shape.\n

        It clips the position of the shape to be between -`utils.BORDER` and `utils.BORDER`.
        It wraps the rotation of the shape to be between `-2 * numpy.pi` and `2 * numpy.pi`.
        It clips the size of the shape to be between `0.000001` and `utils.BORDER`.\n

        Parameters:
            pos (pyrr.Vector3 | None): The position of the shape. If None, the position is not changed.
            rot (pyrr.Vector3 | None): The rotation of the shape. If None, the rotation is not changed.
            size (pyrr.Vector3 | None): The size of the shape. If None, the size is not changed.
        """
        if pos is not None:
            self.pos = pos
            self.pos = pyrr.Vector3(numpy.clip(self.pos, -utils.BORDER, utils.BORDER), dtype=numpy.single)

        if rot is not None:
            self.rot = rot
            self.rot = pyrr.Vector3(numpy.fmod(self.rot, 2 * numpy.pi), dtype=numpy.single)

        if size is not None:
            self.size = size
            self.size = pyrr.Vector3(numpy.clip(self.size, 0.000001, utils.BORDER), dtype=numpy.single)

    def move(
            self: typing.Self,
            delta: pyrr.Vector3,
            /
            ) -> None:
        """
        Move the shape by the given delta.\n

        It clips the position of the shape to be between -`utils.BORDER` and `utils.BORDER`.\n

        Parameters:
            delta (pyrr.Vector3): The delta to move the shape by.
        """
        self.pos += delta
        self.pos = pyrr.Vector3(numpy.clip(self.pos, -utils.BORDER, utils.BORDER), dtype=numpy.single)

    def rotate(
            self: typing.Self,
            delta: pyrr.Vector3,
            /
            ) -> None:
        """
        Rotate the shape by the given delta.\n

        It wraps the rotation of the shape to be between `-2 * numpy.pi` and `2 * numpy.pi`.\n

        Parameters:
            delta (pyrr.Vector3): The delta to rotate the shape by.
        """
        self.rot += delta
        self.rot = pyrr.Vector3(numpy.fmod(self.rot, 2 * numpy.pi), dtype=numpy.single)

    def scale(
            self: typing.Self,
            value: pyrr.Vector3,
            /
            ) -> None:
        """
        Scale the shape by the given value.\n

        It clips the size of the shape to be between `0.000001` and `utils.BORDER`.\n

        Parameters:
            value (pyrr.Vector3): The value to scale the shape by.
        """
        self.size *= value
        self.size = pyrr.Vector3(numpy.clip(self.size, 0.000001, utils.BORDER), dtype=numpy.single)

    def updateModelMatrix(
            self: typing.Self,
            /,
            *,
            parent_pos: pyrr.Vector3 | None = None,
            parent_rot: pyrr.Vector3 | None = None,
            parent_size: pyrr.Vector3 | None = None
            ) -> None:
        """
        Update the model matrix of the shape.\n

        Parameters:
            parent_pos (pyrr.Vector3 | None): The position of the parent shape. If None, it is not used.
            parent_rot (pyrr.Vector3 | None): The rotation of the parent shape. If None, it is not used.
            parent_size (pyrr.Vector3 | None): The size of the parent shape. If None, it is not used.
        """
        trans_matrix = pyrr.Matrix44.from_translation(self.pos if parent_pos is None else (self.pos + parent_pos), dtype=numpy.single)
        rot_matrix = pyrr.Matrix44.from_eulers(self.rot if parent_rot is None else (self.rot + parent_rot), dtype=numpy.single)
        size_matrix = pyrr.Matrix44.from_scale(self.size if parent_size is None else (self.size * parent_size), dtype=numpy.single)

        self.model = trans_matrix * rot_matrix * size_matrix

    def render(
            self: typing.Self,
            view: pyrr.Matrix44,
            projection: pyrr.Matrix44,
            /
            ) -> None:
        """
        Render the shape using the shader and the mesh.\n

        Parameters:
            view (pyrr.Matrix44): The view matrix to use for rendering.
            projection (pyrr.Matrix44): The projection matrix to use for rendering.
        """
        if self.shader.program is None or self.mesh.vertices.size == 0:
            return

        GL.glUseProgram(self.shader.program)

        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "model"), 1, GL.GL_FALSE, self.model)
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "view"), 1, GL.GL_FALSE, view)
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "projection"), 1, GL.GL_FALSE, projection)

        GL.glBindVertexArray(self.mesh.vao)

        if self.material is not None:
            # TODO
            pass
        if self.texture is not None:
            # TODO
            pass
        if self.has_light:
            # TODO
            pass

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.mesh.indices), GL.GL_UNSIGNED_INT, None)

    def cleanRessources(
            self: typing.Self,
            /
            ) -> None:
        """
        Delete all the ressources used by the shape.
        This includes the shader, the mesh, the material and the texture.
        It also removes the shape from its parent if it has one.
        """
        del self.texture
        del self.material
        del self.mesh
        del self.shader

        if self.parent is not None:
            self.parent.subElements(self)
