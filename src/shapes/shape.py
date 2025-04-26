"""
shape module
============
Package: `shapes`

Module to/that # TODO: set docstring

Classes
-------
- `Shape`
"""


# built-in imports
import typing
# pip imports
import pyglm.glm as glm
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, ressources
if typing.TYPE_CHECKING:
    from . import Node


class Shape:
    """
    Shape class
    ===========

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `setShader`
    - `setMesh`
    - `setTexture`
    - `switchLight`
    - `setCoord`
    - `move`
    - `rotate`
    - `scale`
    - `updateModelMatrix`
    - `render`
    - `cleanRessources`
    """
    def __init__(
            self: typing.Self,
            parent: "Node | None" = None,
            /,
            *,
            shader_name: str = "",
            mesh_name: str = "",
            texture_name: str = "",
            has_light: bool = False
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`Node | None`): Parent of this shape, if it is inside a graph.
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this shape use lights.
        Raises:
            # TODO: set exceptions
        """
        self.parent: Node | None = parent
        self.parent_key: str = ""

        self.pos: glm.vec3 = glm.vec3(0)
        self.rot: glm.vec3 = glm.vec3(0)
        self.size: glm.vec3 = glm.vec3(1)

        self.shader: ressources.Shader | None = None
        self.mesh: ressources.Mesh | None = None
        self.texture: ressources.Texture | None = None
        self.has_light: bool = False

        self.model: glm.mat4x4 = glm.mat4x4()

        self.to_update: bool = True
        self.to_render: bool = True

        self.setShader(shader_name)
        self.setMesh(mesh_name)
        self.setTexture(texture_name)
        self.switchLight(has_light)

        self.updateModelMatrix()

    def setShader(
            self: typing.Self,
            shader_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
        Raises:
            # TODO: set exceptions
        """
        if self.shader is not None:
            self.shader.clean()

        self.shader = None
        try:
            if shader_name:
                self.shader = ressources.Shader(shader_name)
                self.to_render = True
        except Exception as e:
            print(f"Error loading shader {shader_name}: {e}")
            print("Setting shader to None.")

    def setMesh(
            self: typing.Self,
            mesh_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
        Raises:
            # TODO: set exceptions
        """
        if self.mesh is not None:
            self.mesh.clean()

        self.mesh = None
        try:
            if mesh_name:
                self.mesh = ressources.Mesh(mesh_name)
                self.to_update = True
        except Exception as e:
            print(f"Error loading mesh {mesh_name}: {e}")
            print("Setting mesh to None.")

    def setTexture(
            self: typing.Self,
            texture_name: str = "",
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
        Raises:
            # TODO: set exceptions
        """
        if self.texture is not None:
            self.texture.clean()

        self.texture = None
        try:
            if texture_name:
                self.texture = ressources.Texture(texture_name)
                self.to_render = True
        except Exception as e:
            print(f"Error loading texture {texture_name}: {e}")
            print("Setting texture to None.")

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
        self.has_light = value if value is not None else not self.has_light

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
            pos (`glm.vec3 | None`): New position of the shape.
            rot (`glm.vec3 | None`): New rotation of the shape.
            size (`glm.vec3 | None`): New size of the shape.
        Raises:
            # TODO: set exceptions
        """
        if pos is not None:
            self.pos = glm.clamp(pos, -utils.BORDER, utils.BORDER)
            self.to_update = True

        if rot is not None:
            self.rot = rot % utils.TWO_PI
            self.to_update = True

        if size is not None:
            self.size = glm.clamp(size, 0.000001, utils.BORDER)
            self.to_update = True

    def move(
            self: typing.Self,
            delta: glm.vec3,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta (`glm.vec3`): The movement to apply to shape.
        Raises:
            # TODO: set exceptions
        """
        self.pos += delta
        self.pos = glm.clamp(self.pos, -utils.BORDER, utils.BORDER)
        self.to_update = True

    def rotate(
            self: typing.Self,
            delta: glm.vec3,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta (`glm.vec3`): The rotation to apply to shape.
        Raises:
            # TODO: set exceptions
        """
        self.rot += delta
        self.rot = self.rot % utils.TWO_PI
        self.to_update = True

    def scale(
            self: typing.Self,
            value: glm.vec3,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            value (`glm.vec3`): The scale to apply to shape.
        Raises:
            # TODO: set exceptions
        """
        self.size *= value
        self.size = glm.clamp(self.size, 0.000001, utils.BORDER)
        self.to_update = True

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
        if not (self.to_update or forced):
            return

        self.model = glm.mat4x4()

        self.model = glm.translate(self.model, self.pos if parent_pos is None else (self.pos + parent_pos))

        rot: glm.vec3 = self.rot if parent_rot is None else (self.rot + parent_rot)
        self.model *= glm.mat4_cast(glm.angleAxis(rot.x, utils.YAW_AXIS) * glm.angleAxis(rot.y, utils.PITCH_AXIS) * glm.angleAxis(rot.z, utils.ROLL_AXIS))  # type: ignore

        self.model = glm.scale(self.model, self.size if parent_size is None else (self.size * parent_size))

        self.to_update = False
        self.to_render = True

    def render(
            self: typing.Self,
            view: glm.mat4x4,
            proj: glm.mat4x4,
            forced: bool = False,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            view (`glm.mat4x4`): View matrix of camera to use for render.
            proj (`glm.mat4x4`): Projection matrix of camera to use for render.
            forced (`bool`): If we are forced to render.
        Raises:
            # TODO: set exceptions
        """
        if self.shader is None or self.mesh is None:
            return
        if not (self.to_render or forced):
            return

        GL.glUseProgram(self.shader.program)

        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "model"), 1, GL.GL_FALSE, glm.value_ptr(self.model))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "view"), 1, GL.GL_FALSE, glm.value_ptr(view))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "projection"), 1, GL.GL_FALSE, glm.value_ptr(proj))

        GL.glBindVertexArray(self.mesh.vao)

        if self.texture is not None:
            # TODO
            pass
        if self.has_light:
            # TODO
            pass

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.mesh.indices), GL.GL_UNSIGNED_INT, None)

        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

        self.to_render = False

    def __del__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        self.cleanRessources()

    def cleanRessources(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        if self.texture is not None:
            self.texture.clean()
        if self.mesh is not None:
            self.mesh.clean()
        if self.shader is not None:
            self.shader.clean()

        if self.parent is not None:
            self.parent.subElements(self)
