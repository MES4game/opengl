"""
shader module
=============
Package: `ressources`

Module to/that # TODO: set docstring

Classes
-------
- `Shader`
"""


# built-in imports
import os
import typing
# pip imports
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, Ressource


class Shader(Ressource):
    """
    Shader class
    ============
    Parent class: `Ressource`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `compileShader` (staticmethod)
    """
    @staticmethod
    def compileShader(
            src: str,
            type: typing.Any,
            /
            ) -> typing.Any:
        """
        Method to/that # TODO: set docstring

        Args:
            src (`str`): Absolute path for shader.
            type (`typing.Any`): Type of shader to compile.
        Returns:
            `typing.Any`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        text: str = open(src, "r").read()

        s: typing.Any = GL.glCreateShader(type)
        GL.glShaderSource(s, text)
        GL.glCompileShader(s)

        if not GL.glGetShaderiv(s, GL.GL_COMPILE_STATUS):
            raise Exception(GL.glGetShaderInfoLog(s))

        return s

    @typing.override
    def __init__(
            self: typing.Self,
            shader_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
        Raises:
            # TODO: set exceptions
        """
        super().__init__(shader_name=shader_name)

        shader_path: str = os.path.join(utils.ABS_PATH.shaders, shader_name)
        vert_shader = self.__class__.compileShader(shader_path + utils.EXTENSIONS.shader_vert, GL.GL_VERTEX_SHADER)
        frag_shader = self.__class__.compileShader(shader_path + utils.EXTENSIONS.shader_frag, GL.GL_FRAGMENT_SHADER)

        if not (vert_shader and frag_shader):
            raise Exception("Shader compilation failed.")

        self.program: typing.Any = GL.glCreateProgram()
        GL.glAttachShader(self.program, vert_shader)
        GL.glAttachShader(self.program, frag_shader)
        GL.glLinkProgram(self.program)

        if not GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS):
            raise Exception(GL.glGetProgramInfoLog(self.program))

    @typing.override
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

        GL.glUseProgram(0)
        GL.glDeleteProgram(self.program)
        self.program = None

        return 0
