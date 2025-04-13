# -*- coding: utf-8 -*-
"""
objects package
===============
This package contains shape classes.\n

The classes in this package are:
- `Shape`: A class representing a generic shape.
- `Node`: A class that extends the `Shape` class to represent a shape with children.

It also loads the package `basics` which contains the basic shape classes.
"""


from .. import utils, ressources  # type: ignore # noqa: F401
from .shape import Shape  # type: ignore # noqa: F401
from .node import Node  # type: ignore # noqa: F401
from . import basics  # type: ignore # noqa: F401
