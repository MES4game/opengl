# -*- coding: utf-8 -*-
"""
cone module
===========
This module contains the `Cone` class, which is a subclass of `Shape`.
It represents a cone shape in a 3D scene.\n

By default, the cone is initialized with a shader name of `"scene"` and a mesh name of `"cone"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Cone(Shape):
    """
    Parent class: `Shape`\n

    The `Cone` class is a subclass of the `Shape` class.
    It represents a cone shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Cone` object.\n

        It initializes the cone shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"cone"`.
        """
        super().__init__(shader_name="scene", mesh_name="cone")
