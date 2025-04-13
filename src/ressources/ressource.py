# -*- coding: utf-8 -*-
"""
ressource module
================
This module contains the `Ressource` class, which is a base class for all ressources.\n

When you create a new ressource, it will check if the ressource already exists.
If it does, it will return the existing ressource instead of creating one.\n

The ressource is identified by its `_name`.
The `_name` is build using classmethod `getName`.
The name is build from the kwargs passed to the constructor.
"""


# built-in imports
import typing
# pip imports
# local imports


class Ressource():
    """
    Class to manage the ressources in the program.\n

    When you create a new ressource, it will check if the ressource already exists.
    If it does, it will return the existing ressource instead of creating one.\n

    The ressource is identified by its `_name`.
    The `_name` is build using classmethod `getName`.\n

    Please do not forget to write `__init__` and `__del__` methods like this:\n
        def __init__(self, /, *_, **kwargs: typing.Any) -> None:
            super().__init__()  # Call it with your desired kwargs for getName (do not forget to pass them as keyword args with the same key name)

            # DO WHATEVER YOU WANT TO DO HERE

        def __del__(self) -> None:
            super().__del__()

            # DO WHATEVER YOU WANT TO DO HERE
    """
    _ressources: dict[str, typing.Self]
    _no_name_nb: int = 0

    @classmethod
    def getName(
            cls: type[typing.Self],
            /,
            *args: typing.Any,
            **kwargs: typing.Any
            ) -> str:
        """
        Get the name of the ressource.\n

        It will be used to identify the ressource in the `cls._ressources` dict.
        The name is build from the kwargs passed to the constructor.\n

        The kwargs are sorted by key and concatenated with " / ".
        If the kwarg's value is not a string, it will be ignored.\n

        If no kwargs are passed, the name will be `"no_name_<cls._NO_NAME_NB>"`, and `cls._NO_NAME_NB` will be incremented.\n

        Parameters:
            kwargs (dict[str, typing.Any]): The kwargs passed to the constructor.

        Returns:
            str: The name of the ressource.
        """
        name: str = ""

        for _, value in sorted(kwargs.items()):
            if not isinstance(value, str):
                continue
            name += f"{value} / "

        if not name:
            name = f"no_name_{cls._no_name_nb}"
            cls._no_name_nb += 1
        else:
            name = name[:-3]

        return name

    def __init_subclass__(
            cls: type[typing.Self],
            /
            ) -> None:
        """
        Initialize the class.\n

        It will create the `_ressources` dict and the `_no_name_nb` counter.
        """
        super().__init_subclass__()

        cls._ressources = {}
        cls._no_name_nb = 0

    def __new__(
            cls: type[typing.Self],
            /,
            *args: typing.Any,
            **kwargs: typing.Any
            ) -> typing.Self:
        """
        Create a new instance of the class.\n

        It will check if the ressource already exists.
        If it does, it will return the existing ressource instead of creating one.\n

        The ressource is identified by `cls.getName(**kwargs)`.\n

        Parameters:
            kwargs (dict[str, typing.Any]): The kwargs passed to the constructor.

        Returns:
            typing.Self: The instance of the class.
        """
        name: str = cls.getName(**kwargs)

        if name not in cls._ressources:
            cls._ressources[name] = super().__new__(cls)
        else:
            cls._ressources[name].__alived += 1

        return cls._ressources[name]

    def __init__(
            self: typing.Self,
            /,
            *args: typing.Any,
            **kwargs: typing.Any
            ) -> None:
        """
        Initialize the `Ressource` object.\n

        It will call the `cls.getName` classmethod to get the name of the ressource and save it in `self._name`.
        It will also initialize the `self.__alived` counter to 1.\n

        Parameters:
            kwargs (dict[str, typing.Any]): The kwargs passed to the constructor.
        """
        self._name: str = self.__class__.getName(**kwargs)
        self.__alived: int = 1

    def __del__(
            self: typing.Self,
            /
            ) -> None:
        """
        Delete the instance.\n

        It will decrement the `self.__alived` counter.
        If the counter is 0, it will remove the ressource from the `cls._ressources` dict.
        """
        if self._name in self.__class__._ressources:
            self.__class__._ressources[self._name].__alived -= 1

            if self.__class__._ressources[self._name].__alived > 0:
                return

            self.__class__._ressources.pop(self._name)
