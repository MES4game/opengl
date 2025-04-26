"""
cylinder module
===============
Package: `basics`

Module to/that # TODO: set docstring

Classes
-------
- `Cylinder`
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Shape, Node


class Cylinder(Shape):
    """
    Cylinder class
    ==============
    Parent class: `Shape`

    Class to/that # TODO: set docstring
    """
    @typing.override
    def __init__(
            self: typing.Self,
            parent: Node | None = None,
            /,
            *,
            texture_name: str = "",
            has_light: bool = False
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`Node | None`): Parent of this shape, if it is inside a graph.
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this shape use lights.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(
            parent,
            shader_name="scene",
            mesh_name="cylinder",
            texture_name=texture_name,
            has_light=has_light
        )
