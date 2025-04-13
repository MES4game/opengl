# -*- coding: utf-8 -*-
"""
pyramid module
===========
This module contains the `Pyramid` class, which is a subclass of `Shape`.
It represents a pyramid shape in a 3D scene.\n

By default, the pyramid is initialized with a shader name of `"scene"` and a mesh name of `"pyramid"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Pyramid(Shape):
    """
    Parent class: `Shape`\n

    The `Pyramid` class is a subclass of the `Shape` class.
    It represents a pyramid shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Pyramid` object.\n

        It initializes the pyramid shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"pyramid"`.
        """
        super().__init__(shader_name="scene", mesh_name="pyramid")
