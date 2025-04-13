# -*- coding: utf-8 -*-
"""
scene module
============
This module contains the `Scene` class, which is used to manage the elements in the scene.\n

It allows adding, removing, updating, and rendering elements in the scene.
It also provides a method to clean up resources used by the elements.
"""


# built-in imports
import typing
# pip imports
import pyrr  # type: ignore
# local imports
from . import shapes


class Scene:
    """
    This class is used to manage the elements in the scene.\n

    It allows adding, removing, updating, and rendering elements in the scene.
    It also provides a method to clean up resources used by the elements.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Scene` object.
        """
        self.elements: dict[str, shapes.Shape] = {}
        self._nb_no_name = 0

    def addElements(
            self: typing.Self,
            /,
            *args: shapes.Shape,
            **kwargs: shapes.Shape
            ) -> None:
        """
        Add elements to the scene.\n

        This method adds elements to the scene, either by name or by position in `self.elements`.\n

        If the element is passed as a positional argument, it is added to `self.elements` with the key `"no_name_{self._nb_no_name}"`.
        The `_nb_no_name` attribute is incremented by 1.\n

        If the element is passed as a keyword argument, it is added to `self.elements` with the key it was passed.\n

        Parameters:
            args (tuple[shapes.Shape, ...]): The elements to add to the scene.
            kwargs (dict[str, shapes.Shape]): The elements to add to the scene, with their names as keys.
        """
        for element in args:
            self.elements[f"no_name_{self._nb_no_name}"] = element
            self._nb_no_name += 1

        for name, element in kwargs.items():
            if name in self.elements:
                raise KeyError(f"'{name}' already exists in scene.")
            self.elements[name] = element

    def subElements(
            self: typing.Self,
            /,
            *args: str | shapes.Shape
            ) -> None:
        """
        Remove elements from the scene.\n

        This method removes elements from the scene, either by name or by item.\n

        If the element is passed as a string, it is removed from `self.children` with the key it was passed.
        If the element is passed as an item, it is removed from `self.children` by searching for it in the values of `self.children`.
        If the element is not found, it is ignored.\n

        Parameters:
            args (tuple[str | Shape, ...]): The elements to remove from the scene.
        """
        for arg in args:
            if isinstance(arg, str):
                if arg in self.elements:
                    self.elements.pop(arg)
            else:
                for key, value in self.elements.items():
                    if value is arg:
                        self.elements.pop(key)
                        break

    def updateModelMatrices(
            self: typing.Self,
            /
            ) -> None:
        """
        Update the model matrices of the elements in the scene.
        """
        for element in self.elements.values():
            element.updateModelMatrix()

    def render(
            self: typing.Self,
            view: pyrr.Matrix44,
            proj: pyrr.Matrix44,
            /
            ) -> None:
        """
        Render the scene and its elements.\n

        This method calls the `render` method of each child.\n

        Parameters:
            view (pyrr.Matrix44): The view matrix to use for rendering.
            projection (pyrr.Matrix44): The projection matrix to use for rendering.
        """
        for element in self.elements.values():
            element.render(view, proj)

    def cleanRessources(
            self: typing.Self,
            /
            ) -> None:
        """
        Clean up the resources used by the elements in the scene.\n

        This method calls the `cleanRessources` method of each child.
        It also clears the `self.elements` dictionary.
        """
        for element in self.elements.values():
            element.cleanRessources()

        self.elements.clear()
