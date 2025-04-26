"""
ressource module
================
Package: `ressources`

Module to/that # TODO: set docstring

Classes
-------
- `Ressource`
"""


# built-in imports
import typing
# pip imports
# local imports


class Ressource():
    """
    Ressource class
    ===============

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `getName` (classmethod)
    - `clean`
    """
    @classmethod
    def getName(
            cls: type[typing.Self],
            /,
            **kwargs: typing.Any
            ) -> str:
        """
        Method to/that # TODO: set docstring

        Args:
            **kwargs (`typing.Any`): args to get name of ressource.
        Returns:
            `str`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        name: str = ""

        for _, value in sorted(kwargs.items()):
            if not isinstance(value, str):
                continue
            name += f"{value} / "

        if not name:
            name = f"no_name_{cls.__no_name_nb}"
            cls.__no_name_nb += 1
        else:
            name = name[:-3]

        return name

    def __init_subclass__(
            cls: type[typing.Self],
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        super().__init_subclass__()

        cls.__ressources: dict[str, typing.Self] = {}
        cls.__no_name_nb: int = 0

    def __new__(
            cls: type[typing.Self],
            /,
            *_,
            **kwargs: typing.Any
            ) -> typing.Self:
        """
        Method to/that # TODO: set docstring

        Args:
            **kwargs (`typing.Any`): args to get name of ressource.
        Returns:
            `typing.Self`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        name: str = cls.getName(**kwargs)

        if name not in cls.__ressources:
            cls.__ressources[name] = super().__new__(cls)
        else:
            cls.__ressources[name].__alived += 1

        return cls.__ressources[name]

    def __init__(
            self: typing.Self,
            /,
            **kwargs: typing.Any
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            **kwargs (`typing.Any`): args to get name of ressource.
        Raises:
            # TODO: set exceptions
        """
        self.__name: str = Ressource.getName(**kwargs)
        self.__alived: int = 1

    def __del__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        self.clean()

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
        if self.__name in self.__class__.__ressources:
            self.__class__.__ressources[self.__name].__alived -= 1

            if self.__class__.__ressources[self.__name].__alived > 0:
                return 1

            self.__class__.__ressources.pop(self.__name)

        return 0
