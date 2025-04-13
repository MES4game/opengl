# -*- coding: utf-8 -*-
"""
ressources package
==================
This package is used to manage ressources in the program.
It contains Ressource class and its subclasses.\n

It uses the utils module to get absolute path and extension of ressources.\n

Here are the classes in this package:

- Ressource: The base class for all ressources.

- Shader: The class for shaders:
    - It compiles the shaders from source files.
    - You need to provide the shader `name` (only file name without extensions or any folder).
    - Shaders are compiled from `os.path.join(utils.ABS_PATH.shaders, name + utils.EXTENSIONS.shader_vertex)` and `os.path.join(utils.ABS_PATH.shaders, name + utils.EXTENSIONS.shader_fragment)`.

- Mesh: The class for meshes:
    - It loads the meshes from files.
    - You need to provide the mesh `name` (only file name without extensions or any folder).
    - Meshes are loaded from `os.path.join(utils.ABS_PATH.meshes, name + utils.EXTENSIONS.mesh)`.

- Material: The class for materials:
    - It loads the materials from files.
    - You need to provide the material `name` (only file name without extensions or any folder).
    - Materials are loaded from `os.path.join(utils.ABS_PATH.materials, name + utils.EXTENSIONS.material)`.

- Texture: The class for textures:
    - It loads the textures from files.
    - You need to provide the texture `name` (only file name without extensions or any folder).
    - Textures are loaded from `os.path.join(utils.ABS_PATH.textures, name + utils.EXTENSIONS.texture)`.
"""


from .. import utils  # type: ignore # noqa: F401
from .ressource import Ressource  # type: ignore # noqa: F401
from .shader import Shader  # type: ignore # noqa: F401
from .mesh import Mesh  # type: ignore # noqa: F401
from .material import Material  # type: ignore # noqa: F401
from .texture import Texture  # type: ignore # noqa: F401
