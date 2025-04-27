"""
src package
===========

Package to/that # TODO: set docstring

Sub-packages
------------
- `ressources`
- `shapes`
Modules
-------
- `utils`
Classes
-------
- `Scene`
- `Camera`
- `FPSCamera`
- `FreeCamera`
- `OrbitCamera`
- `TPSCamera`
- `Renderer`
"""


from . import utils, ressources  # type: ignore # noqa: F401
from .camera import Camera, FPSCamera, FreeCamera, OrbitCamera, TPSCamera  # type: ignore # noqa: F401
from . import shapes  # type: ignore # noqa: F401
from .scene import Scene  # type: ignore # noqa: F401
from .renderer import Renderer  # type: ignore # noqa: F401
