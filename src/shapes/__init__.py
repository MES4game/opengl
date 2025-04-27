"""
shapes package
==============
Parent package: `src`

Package to/that # TODO: set docstring

Sub-packages
------------
- `basics`
Modules
-------
- `utils` (from parent package)
- `ressources` (from parent package)
Classes
-------
- `Shape`
- `Node`
"""


from .. import utils, ressources, Camera  # type: ignore # noqa: F401
from .shape import Shape  # type: ignore # noqa: F401
from .node import Node  # type: ignore # noqa: F401
from . import basics  # type: ignore # noqa: F401
