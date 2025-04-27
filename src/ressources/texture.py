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
import os
import typing
# pip imports
import OpenGL.GL as GL  # type: ignore
import PIL.Image
# local imports
from . import utils, Ressource


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
            ) -> tuple[int, int, bytes]:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for texture.
        Returns:
            `tuple[int,int,bytes]`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        image: PIL.Image.Image = PIL.Image.open(src)
        return image.width, image.height, image.convert("RGBA").tobytes()

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

        width, height, data = Texture.loadTexture(os.path.join(utils.ABS_PATH.textures, texture_name + utils.EXTENSIONS.texture))

        self.id: typing.Any = GL.glGenTextures(1)

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width, height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

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

        GL.glDeleteTextures(1, (self.id,))

        return 0
