# -*- coding: utf-8 -*-
"""
cube module
===========
This module contains the `Cube` class, which is a subclass of `Shape`.
It represents a cube shape in a 3D scene.\n

By default, the cube is initialized with a shader name of `"scene"` and a mesh name of `"cube"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Cube(Shape):
    """
    Parent class: `Shape`\n

    The `Cube` class is a subclass of the `Shape` class.
    It represents a cube shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Cube` object.\n

        It initializes the cube shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"cube"`.
        """
        super().__init__(shader_name="scene", mesh_name="cube")
