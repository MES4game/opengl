# -*- coding: utf-8 -*-
"""
node module
===========
This module contains the `Node` class, which is a subclass of `Shape`.\n

It is used to represent a node in the scene graph, which can have children shapes.
It allows for hierarchical transformations, where the position, rotation and size of a node affect its children.
"""


# built-in imports
import typing
# pip imports
import numpy
import pyrr  # TODO # type: ignore
# local imports
from . import Shape


class Node(Shape):
    """
    Parent class: `Shape`\n

    Class to represent a node in the scene graph.\n

    It is used to represent a node in the scene graph, which can have children shapes.
    It allows for hierarchical transformations, where the position, rotation and size of a node affect its children.\n
    """
    def __init__(
            self: typing.Self,
            /,
            *,
            parent: typing.Self | None = None,
            shader_name: str = "",
            mesh_name: str = ""
            ) -> None:
        """
        Initialize the `Node` object.\n

        This method initializes the position, rotation and size of the node, as well as the shader and the mesh to use for rendering.
        It also initializes the material and the texture to None.\n

        It also initializes the children of the node to an empty dictionary.
        And the number of unnamed children to 0.\n

        Parameters:
            parent (typing.Self | None): The parent of the node. If None, the node is not attached to any parent.
            shader_name (str): The name of the shader file (without extension) to use for rendering the node.
            mesh_name (str): The name of the mesh file (without extension) to use for rendering the node.
        """
        self.children: dict[str, Shape] = {}
        self._nb_no_name = 0

        super().__init__(parent=parent, shader_name=shader_name, mesh_name=mesh_name)

    def addElements(
            self: typing.Self,
            /,
            *args: Shape,
            **kwargs: Shape
            ) -> None:
        """
        Add elements to the node.\n

        This method adds elements to the node, either by name or by position in `self.children`.\n

        If the element is passed as a positional argument, it is added to `self.children` with the key `"no_name_{self._nb_no_name}"`.
        The `_nb_no_name` attribute is incremented by 1.\n

        If the element is passed as a keyword argument, it is added to `self.children` with the key it was passed.\n

        Parameters:
            args (tuple[Shape, ...]): The elements to add to the node.
            kwargs (dict[str, Shape]): The elements to add to the node, with their names as keys.
        """
        for element in args:
            self.children[f"no_name_{self._nb_no_name}"] = element
            self._nb_no_name += 1

            if element.parent is not None:
                element.parent.subElements(element)
            element.parent = self

        for name, element in kwargs.items():
            if name in self.children:
                raise KeyError(f"'{name}' already exists in Node '{self}'.")
            self.children[name] = element

            if element.parent is not None:
                element.parent.subElements(element)
            element.parent = self

    def subElements(
            self: typing.Self,
            /,
            *args: str | Shape
            ) -> None:
        """
        Remove elements from the node.\n

        This method removes elements from the node, either by name or by item.\n

        If the element is passed as a string, it is removed from `self.children` with the key it was passed.
        If the element is passed as an item, it is removed from `self.children` by searching for it in the values of `self.children`.
        If the element is not found, it is ignored.\n

        Parameters:
            args (tuple[str | Shape, ...]): The elements to remove from the node.
        """
        for arg in args:
            if isinstance(arg, str):
                if arg in self.children:
                    self.children.pop(arg)
            else:
                for key, value in self.children.items():
                    if value is arg:
                        self.children.pop(key)
                        break

    def setCoord(
            self: typing.Self,
            /,
            *,
            pos: pyrr.Vector3 | None = None,
            rot: pyrr.Vector3 | None = None,
            size: pyrr.Vector3 | None = None
            ) -> None:
        """
        Set the coordinates of the node.\n

        This method sets the position, rotation and size of the node.
        It also updates the position of the children of the node, if necessary.\n

        Parameters:
            pos (pyrr.Vector3 | None): The position of the node. If None, the position is not changed.
            rot (pyrr.Vector3 | None): The rotation of the node. If None, the rotation is not changed.
            size (pyrr.Vector3 | None): The size of the node. If None, the size is not changed.
        """
        old_rot = self.rot
        old_size = self.size

        super().setCoord(pos=pos, rot=rot, size=size)

        delta_rot = self.rot - old_rot
        rot_matrix = pyrr.Matrix33.from_eulers(pyrr.euler.create(*(delta_rot * [1.0, 1.0, -1.0]), dtype=numpy.single))
        delta_size = self.size / old_size

        for child in self.children.values():
            child.setCoord(pos=pyrr.Vector3(rot_matrix @ child.pos))
            child.setCoord(pos=pyrr.Vector3(child.pos * delta_size))

    def rotate(
            self: typing.Self,
            delta: pyrr.Vector3,
            /
            ) -> None:
        """
        Rotate the node by the given delta.\n

        This method updates the rotation of the node and the position of its children.\n

        Parameters:
            delta (pyrr.Vector3): The delta to rotate the node by.
        """
        super().rotate(delta)

        rot_matrix = pyrr.Matrix33.from_eulers(pyrr.euler.create(*(delta * [1.0, 1.0, -1.0]), dtype=numpy.single))
        for child in self.children.values():
            child.setCoord(pos=pyrr.Vector3(rot_matrix @ child.pos))

    def scale(
            self: typing.Self,
            value: pyrr.Vector3,
            /
            ) -> None:
        """
        Scale the node by the given value.\n

        This method updates the size of the node and the position of its children.\n

        Parameters:
            value (pyrr.Vector3): The value to scale the node by.
        """
        super().scale(value)

        for child in self.children.values():
            child.setCoord(pos=pyrr.Vector3(child.pos * value))

    def updateModelMatrix(
            self: typing.Self,
            /,
            *,
            parent_pos: pyrr.Vector3 | None = None,
            parent_rot: pyrr.Vector3 | None = None,
            parent_size: pyrr.Vector3 | None = None
            ) -> None:
        """
        Update the model matrix of the node and its children.\n

        Parameters:
            parent_pos (pyrr.Vector3 | None): The position of the parent node. If None, it is not used.
            parent_rot (pyrr.Vector3 | None): The rotation of the parent node. If None, it is not used.
            parent_size (pyrr.Vector3 | None): The size of the parent node. If None, it is not used.
        """
        super().updateModelMatrix(
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            parent_size=parent_size
        )

        for_child_pos = self.pos if parent_pos is None else (self.pos + parent_pos)
        for_child_rot = self.rot if parent_rot is None else (self.rot + parent_rot)
        for_child_size = self.size if parent_size is None else (self.size * parent_size)

        for child in self.children.values():
            child.updateModelMatrix(
                parent_pos=for_child_pos,
                parent_rot=for_child_rot,
                parent_size=for_child_size
            )

    def render(
            self: typing.Self,
            view: pyrr.Matrix44,
            projection: pyrr.Matrix44,
            /
            ) -> None:
        """
        Render the node and its children.\n

        This method calls the `render` method of the parent class and then calls the `render` method of each child.\n

        Parameters:
            view (pyrr.Matrix44): The view matrix to use for rendering.
            projection (pyrr.Matrix44): The projection matrix to use for rendering.
        """
        super().render(view, projection)

        for child in self.children.values():
            child.render(view, projection)

    def cleanRessources(
            self: typing.Self,
            /
            ) -> None:
        """
        Clean the resources of the node and its children.\n

        This method calls the `cleanRessources` method of the parent class and then clears the children of the node.
        """
        for child in self.children.values():
            child.cleanRessources()
        self.children.clear()

        super().cleanRessources()
