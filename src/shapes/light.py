"""
shape module
============
Package: `shapes`

Module to/that # TODO: set docstring

Classes
-------
- `Light`
"""


# built-in imports
import typing
# pip imports
import pyglm.glm as glm
# local imports
from . import Shape
if typing.TYPE_CHECKING:
    from . import Node


class Light(Shape):
    """
    Light class
    ===========

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
        # TODO: set methods
    """
    def __init__(
            self: typing.Self,
            parent: "Node | None" = None,
            /,
            *,
            shader_name: str = "",
            mesh_name: str = "",
            color: glm.vec3 | None = None,
            texture_name: str = "",
            has_light: bool = False,
            light_color: glm.vec3 = glm.vec3(1)
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`Node | None`): Parent of this shape, if it is inside a graph.
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
            color (`glm.vec3 | None`): Color of the node, if None, set to white by default.
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this shape use lights.
            light_color (`glm.vec3`): Color of the light, default is white (1, 1, 1).
        Raises:
            # TODO: set exceptions
        """
        super().__init__(
            parent,
            shader_name=shader_name,
            mesh_name=mesh_name,
            color=color,
            texture_name=texture_name,
            has_light=has_light
        )

        self.light_color = light_color

    def setLightColor(
            self: typing.Self,
            light_color: glm.vec3 | None = None,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            light_color (`glm.vec3 | None`): Color of the light, if None, set to white by default.
        Raises:
            # TODO: set exceptions
        """
        self.light_color = light_color if light_color is not None else glm.vec3(1)
        self.to_render = True
