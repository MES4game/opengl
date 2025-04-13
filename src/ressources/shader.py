# -*- coding: utf-8 -*-
"""
shader module
=============
This module contains the `Shader` class, which is used to load and compile shaders for OpenGL rendering.\n

It creates the `Shader` class as a subclass of `Ressource`, which is a base class for all resources in the application.\n

The `Shader` class has methods to compile vertex and fragment shaders from source files, link them into a program, and clean up resources when the object is deleted.
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
    Parent class: `Ressource`\n

    Class to compile and load a shader for OpenGL.\n

    If you instantiate the class with a shader name, it will compile the shader and link it to a program.
    If you instantiate the class with `shader_name=""`, it will set `self.program` to `None`.\n

    When the object is deleted, it will delete the program.
    """
    @classmethod
    def compileShader(
            cls: type[typing.Self],
            src: str,
            type: typing.Any,
            /
            ) -> typing.Any:
        """
        Compile a shader from source code.
        It reads the shader source code from a `os.path.join(utils.ABS_PATH.shaders, src)` file.\n

        Parameters:
            src (str): The name of the shader source file (with extension).
            type (typing.Any): The type of the shader (`GL.GL_VERTEX_SHADER` or `GL.GL_FRAGMENT_SHADER`).

        Returns:
            typing.Any: The compiled shader object.
        """
        text = open(os.path.join(utils.ABS_PATH.shaders, src), "r").read()

        s = GL.glCreateShader(type)
        GL.glShaderSource(s, text)
        GL.glCompileShader(s)

        if not GL.glGetShaderiv(s, GL.GL_COMPILE_STATUS):
            raise Exception(GL.glGetShaderInfoLog(s))

        return s

    def __init__(
            self: typing.Self,
            /,
            *,
            shader_name: str = ""
            ) -> None:
        """
        Initialize the `Shader` object.\n

        If `shader_name` is an empty string, set `self.program` to `None`.
        If `shader_name` is not an empty string, compile the vertex and fragment shaders and link them into a program.\n

        Parameters:
            shader_name (str): The name of the shader (without extension).
        """
        super().__init__(shader_name=shader_name)

        if shader_name == "":
            self.program = None
            return

        vert_shader = self.__class__.compileShader(shader_name + utils.EXTENSIONS.shader_vert, GL.GL_VERTEX_SHADER)
        frag_shader = self.__class__.compileShader(shader_name + utils.EXTENSIONS.shader_frag, GL.GL_FRAGMENT_SHADER)

        if not (vert_shader and frag_shader):
            raise Exception("Shader compilation failed.")

        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, vert_shader)
        GL.glAttachShader(self.program, frag_shader)
        GL.glLinkProgram(self.program)

        if not GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS):
            raise Exception(GL.glGetProgramInfoLog(self.program))

    def __del__(
            self: typing.Self,
            /
            ) -> None:
        """
        Clean up the Shader object.
        Set OpenGL used program to 0 and delete the `self.program`.
        """
        super().__del__()

        GL.glUseProgram(0)
        GL.glDeleteProgram(self.program)
        self.program = None
