# -*- coding: utf-8 -*-
"""
basics package
==============
This package contains basic shapes class.\n

The classes in this package are:
- `Triangle`: A class representing a triangle shape.
- `Square`: A class representing a square shape.
- `Cube`: A class representing a cube shape.
- `Pyramid`: A class representing a pyramid shape.
- `Cone`: A class representing a cone shape.
- `Cylinder`: A class representing a cylinder shape.
- `Sphere`: A class representing a sphere shape.

These classes are all subclasses of the `Shape` class, which is defined in the parent package.
"""


from .. import Shape  # type: ignore # noqa: F401
from .triangle import Triangle  # type: ignore # noqa: F401
from .square import Square  # type: ignore # noqa: F401
from .cube import Cube  # type: ignore # noqa: F401
from .pyramid import Pyramid  # type: ignore # noqa: F401
from .cone import Cone  # type: ignore # noqa: F401
from .cylinder import Cylinder  # type: ignore # noqa: F401
from .sphere import Sphere  # type: ignore # noqa: F401
