# -*- coding: utf-8 -*-
"""
cylinder module
===========
This module contains the `Cylinder` class, which is a subclass of `Shape`.
It represents a cylinder shape in a 3D scene.\n

By default, the cylinder is initialized with a shader name of `"scene"` and a mesh name of `"cylinder"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Cylinder(Shape):
    """
    Parent class: `Shape`\n

    The `Cylinder` class is a subclass of the `Shape` class.
    It represents a cylinder shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Cylinder` object.\n

        It initializes the cylinder shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"cylinder"`.
        """
        super().__init__(shader_name="scene", mesh_name="cylinder")
