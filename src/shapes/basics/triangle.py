# -*- coding: utf-8 -*-
"""
triangle module
===========
This module contains the `Triangle` class, which is a subclass of `Shape`.
It represents a triangle shape in a 3D scene.\n

By default, the triangle is initialized with a shader name of `"scene"` and a mesh name of `"triangle"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Triangle(Shape):
    """
    Parent class: `Shape`\n

    The `Triangle` class is a subclass of the `Shape` class.
    It represents a triangle shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Triangle` object.\n

        It initializes the triangle shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"triangle"`.
        """
        super().__init__(shader_name="scene", mesh_name="triangle")
