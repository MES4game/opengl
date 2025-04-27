"""
sphere module
=============
Package: `basics`

Module to/that # TODO: set docstring

Classes
-------
- `Sphere`
"""


# built-in imports
import typing
# pip imports
import pyglm.glm as glm
# local imports
from . import Shape, Node


class Sphere(Shape):
    """
    Sphere class
    ============
    Parent class: `Shape`

    Class to/that # TODO: set docstring
    """
    @typing.override
    def __init__(
            self: typing.Self,
            parent: Node | None = None,
            /,
            *,
            color: glm.vec3 | None = None,
            texture_name: str = "",
            has_light: bool = False
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`Node | None`): Parent of this shape, if it is inside a graph.
            color (`glm.vec3 | None`): Color of the node, if None, set to white by default.
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this shape use lights.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(
            parent,
            shader_name=f"basic{"_texlight" if (texture_name and has_light) else ("_tex" if texture_name else ("_light") if has_light else "")}",
            mesh_name="sphere",
            color=color,
            texture_name=texture_name,
            has_light=has_light
        )
