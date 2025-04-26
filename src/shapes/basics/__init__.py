"""
basics package
==============
Parent package: `shapes`

Package to/that # TODO: set docstring

Classes
-------
- `Shape` (from parent package)
- `Node` (from parent package)
- `Triangle`
- `Square`
- `Cube`
- `Pyramid`
- `Cone`
- `Cylinder`
- `Sphere`
"""


from .. import Shape, Node  # type: ignore # noqa: F401
from .triangle import Triangle  # type: ignore # noqa: F401
from .square import Square  # type: ignore # noqa: F401
from .cube import Cube  # type: ignore # noqa: F401
from .pyramid import Pyramid  # type: ignore # noqa: F401
from .cone import Cone  # type: ignore # noqa: F401
from .cylinder import Cylinder  # type: ignore # noqa: F401
from .sphere import Sphere  # type: ignore # noqa: F401
