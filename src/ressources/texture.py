"""
texture module
==============
Package: `ressources`

Module to/that # TODO: set docstring

Classes
-------
- `Texture`
"""


# built-in imports
import typing
# pip imports
# local imports
from . import Ressource


class Texture(Ressource):
    """
    Texture class
    =============
    Parent class: `Ressource`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `loadTexture` (staticmethod)
    """
    @staticmethod
    def loadTexture(
            src: str,
            /
            ) -> typing.Any:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for texture.
        Returns:
            `typing.Any`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        s: typing.Any = None
        # TODO
        return s

    def __init__(
            self: typing.Self,
            texture_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
        Raises:
            # TODO: set exceptions
        """
        super().__init__(texture_name=texture_name)

        # TODO

    def clean(
            self: typing.Self,
            /
            ) -> int:
        """
        Method to/that # TODO: set docstring

        Returns:
            `int`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        if super().clean():
            return 1

        # TODO

        return 0
