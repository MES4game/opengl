"""
scene module
============
Package: `src`

Module to/that # TODO: set docstring

Classes
-------
- `Scene`
"""


# built-in imports
import typing
# pip imports
import pyglm.glm as glm
# local imports
from . import shapes


class Scene(shapes.Node):
    """
    Scene class
    ===========
    Parent class: `shapes.Node`

    Class to/that # TODO: set docstring
    """
    @typing.override
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        super().__init__()
        self._is_scene = True

    @typing.override
    def moveChildren(
            self: typing.Self,
            rot_quat: glm.quat | None = None,
            scale: glm.vec3 | None = None,
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def setShader(
            self: typing.Self,
            shader_name: str = "",
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def setMesh(
            self: typing.Self,
            mesh_name: str = "",
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def setTexture(
            self: typing.Self,
            texture_name: str = "",
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def switchLight(
            self: typing.Self,
            value: bool | None = None,
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def setCoord(
            self: typing.Self,
            /,
            *,
            pos: glm.vec3 | None = None,
            rot: glm.vec3 | None = None,
            size: glm.vec3 | None = None
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def move(
            self: typing.Self,
            delta: glm.vec3,
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def rotate(
            self: typing.Self,
            delta: glm.vec3,
            /
            ) -> None:
        """
        DO NOTHING
        """
        return

    @typing.override
    def scale(
            self: typing.Self,
            value: glm.vec3,
            /
            ) -> None:
        """
        DO NOTHING
        """
        return
