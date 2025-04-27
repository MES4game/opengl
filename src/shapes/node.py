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
from . import utils, Camera, Shape


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

    def moveChildren(
            self: typing.Self,
            rot_quat: glm.quat | None,
            scale: glm.vec3 | None,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            rot_quat (`glm.quat | None`): Rotation (as quaternion) applied to this node.
            scale (`glm.vec3 | None`): Scale applied to this node.
        Raises:
            # TODO: set exceptions
        """
        if rot_quat is None and scale is None:
            return

        for child in self.children.values():
            if rot_quat is not None:
                child.setCoord(pos=glm.vec3(rot_quat * child.pos))

            if scale is not None:
                child.setCoord(pos=glm.vec3(child.pos * scale))

            if isinstance(child, Node):
                child.moveChildren(rot_quat, scale)

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
    def setCoord(
            self: typing.Self,
            /,
            *,
            pos: glm.vec3 | None = None,
            rot: glm.vec3 | None = None,
            size: glm.vec3 | None = None
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            pos (`glm.vec3 | None`): New position of the node.
            rot (`glm.vec3 | None`): New rotation of the node.
            size (`glm.vec3 | None`): New size of the node.
        Raises:
            # TODO: set exceptions
        """
        old_rot = self.rot
        old_size = self.size

        super().setCoord(pos=pos, rot=rot, size=size)

        if rot is None and size is None:
            return

        delta_rot = self.rot - old_rot
        self.moveChildren(
            (glm.angleAxis(delta_rot.x, utils.YAW_AXIS) * glm.angleAxis(delta_rot.y, utils.PITCH_AXIS) * glm.angleAxis(delta_rot.z, utils.ROLL_AXIS)) if rot is not None else None,
            (self.size / old_size) if size is not None else None
        )

    @typing.override
    def rotate(
            self: typing.Self,
            delta: glm.vec3,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta (`glm.vec3`): The rotation to apply to node.
        Raises:
            # TODO: set exceptions
        """
        super().rotate(delta)

        self.moveChildren(glm.angleAxis(delta.x, utils.YAW_AXIS) * glm.angleAxis(delta.y, utils.PITCH_AXIS) * glm.angleAxis(delta.z, utils.ROLL_AXIS), None)

    @typing.override
    def scale(
            self: typing.Self,
            value: glm.vec3,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            value (`glm.vec3`): The scale to apply to node.
        Raises:
            # TODO: set exceptions
        """
        super().scale(value)

        self.moveChildren(None, value)

    @typing.override
    def updateModelMatrix(
            self: typing.Self,
            forced: bool = False,
            /,
            *,
            parent_pos: glm.vec3 | None = None,
            parent_rot: glm.vec3 | None = None,
            parent_size: glm.vec3 | None = None
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            forced (`bool`): If we are forced to recalculate model matrix.
            parent_pos (`glm.vec3 | None`): Parent position to transform relative position to an absolute position.
            parent_rot (`glm.vec3 | None`): Parent rotation to transform relative rotation to an absolute position.
            parent_size (`glm.vec3 | None`): Parent size to transform relative size to an absolute position.
        Raises:
            # TODO: set exceptions
        """
        updated: bool = self.to_update or forced
        super().updateModelMatrix(
            forced,
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            parent_size=parent_size
        )

        for_child_pos: glm.vec3 = self.pos if parent_pos is None else (self.pos + parent_pos)
        for_child_rot: glm.vec3 = self.rot if parent_rot is None else (self.rot + parent_rot)
        for_child_size: glm.vec3 = self.size if parent_size is None else (self.size * parent_size)

        for child in self.children.values():
            child.updateModelMatrix(
                updated,
                parent_pos=for_child_pos,
                parent_rot=for_child_rot,
                parent_size=for_child_size
            )

    @typing.override
    def render(
            self: typing.Self,
            cam: Camera,
            forced: bool = False,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            cam (`Camera`): The camera to take pos, view and proj to render.
            forced (`bool`): If we are forced to render.
        Raises:
            # TODO: set exceptions
        """
        super().render(cam, forced)

        for child in self.children.values():
            child.render(cam, forced)

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
        for child in self.children.values():
            child.cleanRessources()
        self.children.clear()

        super().cleanRessources()
