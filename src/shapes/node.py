"""
node module
===========
Package: `shapes`

Module to/that # TODO: set docstring

Classes
-------
- `Node`
"""


# built-in imports
import typing
# pip imports
import pyglm.glm as glm
# local imports
from . import Shape
if typing.TYPE_CHECKING:
    from .. import Renderer


class Node(Shape):
    """
    Node class
    ==========
    Parent class: `Shape`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `addElements`
    - `subElements`
    - `moveChildren`
    - `switchLight`
    - `setCoord`
    - `rotate`
    - `scale`
    - `updateModelMatrix`
    - `render`
    - `cleanRessources`
    """
    @typing.override
    def __init__(
            self: typing.Self,
            parent: typing.Self | None = None,
            /,
            *,
            shader_name: str = "",
            mesh_name: str = "",
            color: glm.vec3 | None = None,
            texture_name: str = "",
            has_light: bool = False
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`typing.Self | None`): Parent of this shape, if it is inside a graph.
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
            color (`glm.vec3 | None`): Color of the node, if None, set to white by default.
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this node use lights.
        Raises:
            # TODO: set exceptions
        """
        self.children: dict[str, Shape] = {}
        self.__nb_no_name: int = 0
        self._is_scene: bool = False

        super().__init__(
            parent,
            shader_name=shader_name,
            mesh_name=mesh_name,
            color=color,
            texture_name=texture_name,
            has_light=has_light
        )

    def addElements(
            self: typing.Self,
            /,
            *args: Shape,
            **kwargs: Shape
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            *args (`Shape`): elements to add without a specific name.
            **kwargs (`Shape`): elements to add with a specific name.
        Raises:
            # TODO: set exceptions
        """
        for element in args:
            if element.parent is not None:
                element.parent.subElements(element)

            self.children[f"no_name_{self.__nb_no_name}"] = element
            element.parent_key = f"no_name_{self.__nb_no_name}"
            element.parent = self
            if not self._is_scene:
                element.switchLight(self.has_light)
            element.to_update = True

            self.__nb_no_name += 1

        for name, element in kwargs.items():
            if name in self.children:
                print(f"Warning: '{name}' already exists in Node '{self.parent_key}'.")
                continue

            if element.parent is not None:
                element.parent.subElements(element)

            self.children[name] = element
            element.parent_key = name
            element.parent = self
            if not self._is_scene:
                element.switchLight(self.has_light)
            element.to_update = True

    def subElements(
            self: typing.Self,
            /,
            *args: Shape
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            *args (`Shape`): elements to sub from this node.
        Raises:
            # TODO: set exceptions
        """
        for arg in args:
            try:
                self.children.pop(arg.parent_key)
            except KeyError:
                for key, value in self.children.items():
                    if value is arg:
                        self.children.pop(key)
                        break

    @typing.override
    def switchLight(
            self: typing.Self,
            value: bool | None = None,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            value (`bool | None`): Value to set light, if None, just switch it.
        Raises:
            # TODO: set exceptions
        """
        super().switchLight(value)

        for child in self.children.values():
            child.switchLight(self.has_light)

    @typing.override
    def updateModelMatrix(
            self: typing.Self,
            forced: bool = False,
            /,
            *,
            parent_model: glm.mat4x4 | None = None
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            forced (`bool`): If we are forced to recalculate model matrix.
            parent_model (`glm.mat4x4 | None`): Parent model matrix to transform relative model to an absolute model.
        Raises:
            # TODO: set exceptions
        """
        updated: bool = self.to_update or forced
        super().updateModelMatrix(
            forced,
            parent_model=parent_model
        )

        for child in self.children.values():
            child.updateModelMatrix(
                updated,
                parent_model=self.model
            )

    @typing.override
    def render(
            self: typing.Self,
            renderer: "Renderer",
            forced: bool = False,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            renderer (`Renderer`): The renderer to take sun for light and camera for pos, view and proj to render.
            forced (`bool`): If we are forced to render.
        Raises:
            # TODO: set exceptions
        """
        super().render(renderer, forced)

        for child in self.children.values():
            child.render(renderer, forced)

    @typing.override
    def cleanRessources(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        for child in list(self.children.values()):
            child.cleanRessources()
        self.children.clear()

        super().cleanRessources()
