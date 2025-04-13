# -*- coding: utf-8 -*-
"""
sphere module
===========
This module contains the `Sphere` class, which is a subclass of `Shape`.
It represents a sphere shape in a 3D scene.\n

By default, the sphere is initialized with a shader name of `"scene"` and a mesh name of `"sphere"`.
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape


class Sphere(Shape):
    """
    Parent class: `Shape`\n

    The `Sphere` class is a subclass of the `Shape` class.
    It represents a sphere shape in a 3D scene.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Sphere` object.\n

        It initializes the sphere shape with a shader and mesh name.
        The shader name is set to `"scene"` and the mesh name is set to `"sphere"`.
        """
        super().__init__(shader_name="scene", mesh_name="sphere")
