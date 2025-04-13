# -*- coding: utf-8 -*-
"""
square module
===========
This module contains the `Square` class, which is a subclass of `Shape`.
It represents a square shape in a 3D scene.\n

By default, the square is initialized with a shader name of `"scene"` and a mesh name of `"square"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Square(Shape):
    """
    Parent class: `Shape`\n

    The `Square` class is a subclass of the `Shape` class.
    It represents a square shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Square` object.\n

        It initializes the square shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"square"`.
        """
        super().__init__(shader_name="scene", mesh_name="square")
