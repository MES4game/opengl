# -*- coding: utf-8 -*-
"""
source package
==============
This package contains the source code of the OpenGL project.\n

It contains the following modules:
- utils: utility globals, functions and classes for the project.
- ressources: load and manage the resources of the project (shaders, meshes, etc.).
- shapes: classes to create and manage the shapes of the project (Shape, Node, etc.).

It contains the following classes:
- Scene: class to manage the scene of the project (every displayed elements/shapes).
- Camera: class to manage the camera of the project (FPSCamera, FreeCamera, OrbitCamera, TPSCamera).
- Renderer: class to manage everything related to the rendering of the project (window, camera, scene, etc.).
"""


from . import utils, ressources, shapes  # type: ignore # noqa: F401
from .scene import Scene  # type: ignore # noqa: F401
from .camera import Camera, FPSCamera, FreeCamera, OrbitCamera, TPSCamera  # type: ignore # noqa: F401
from .renderer import Renderer  # type: ignore # noqa: F401
