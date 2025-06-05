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
    from . import Node, Renderer


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
            color: glm.vec3 | None = None,
            texture_name: str = "",
            has_light: bool = False
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            parent (`Node | None`): Parent of this shape, if it is inside a graph.
            shader_name (`str`): File name of the shader (without extension and relative to `shaders` folder).
            mesh_name (`str`): File name of the mesh (without extension and relative to `meshes` folder).
            color (`glm.vec3 | None`): Color of the node, if None, set to white by default.
            texture_name (`str`): File name of the texture (without extension and relative to `textures` folder).
            has_light (`bool`): If this shape use lights.
        Raises:
            # TODO: set exceptions
        """
        self.parent: Node | None = parent
        self.parent_key: str = ""

        self.pos: glm.vec3 = glm.vec3(0)
        self.rot: glm.quat = glm.quat()
        self.size: glm.vec3 = glm.vec3(1)

        self.shader: ressources.Shader | None = None
        self.mesh: ressources.Mesh | None = None
        self.color: glm.vec3 = color if color is not None else glm.vec3(1)
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

    def setColor(
            self: typing.Self,
            color: glm.vec3 | None = None,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            color (`glm.vec3 | None`): Color of the node, if None, set to white by default.
        Raises:
            # TODO: set exceptions
        """
        self.color = color if color is not None else glm.vec3(1, 1, 1)
        self.to_render = True

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
            rot: glm.quat | None = None,
            size: glm.vec3 | None = None
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            pos (`glm.vec3 | None`): New position of the shape.
            rot (`glm.quat | None`): New rotation of the shape.
            size (`glm.vec3 | None`): New size of the shape.
        Raises:
            # TODO: set exceptions
        """
        if pos is not None:
            self.pos = glm.clamp(pos, -utils.BORDER, utils.BORDER)
            self.to_update = True

        if rot is not None:
            self.rot = rot
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
            delta: glm.quat,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta (`glm.quat`): The rotation to apply to shape.
        Raises:
            # TODO: set exceptions
        """
        self.rot = delta * self.rot
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
        if not (self.to_update or forced):
            return

        self.model = glm.translate(glm.mat4x4(), self.pos)
        self.model *= glm.mat4_cast(self.rot)  # type: ignore
        self.model = glm.scale(self.model, self.size)
        if parent_model is not None:
            self.model = parent_model * self.model  # type: ignore

        self.to_update = False
        self.to_render = True

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
        if self.shader is None or self.mesh is None:
            return
        if not (self.to_render or forced):
            return

        GL.glUseProgram(self.shader.program)

        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "model_mat4"), 1, GL.GL_FALSE, glm.value_ptr(self.model))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "view_mat4"), 1, GL.GL_FALSE, glm.value_ptr(renderer.camera.view))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.shader.program, "proj_mat4"), 1, GL.GL_FALSE, glm.value_ptr(renderer.camera.proj))

        GL.glBindVertexArray(self.mesh.vao)

        if self.texture is not None:
            GL.glActiveTexture(GL.GL_TEXTURE0)  # Don't need to set it, every shapes are drawn after each other, maybe later if we want multiple textures for one shape
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.id)
            GL.glUniform1i(GL.glGetUniformLocation(self.shader.program, "texture_2D"), 0)
        else:
            GL.glUniform3fv(GL.glGetUniformLocation(self.shader.program, "color_vec3"), 1, glm.value_ptr(self.color))

        if self.has_light:
            GL.glUniform1i(GL.glGetUniformLocation(self.shader.program, "num_lights"), len(renderer.lights))
            for i, (pos, color) in enumerate(map(lambda light: (light.pos, light.light_color), renderer.lights)):
                GL.glUniform3fv(GL.glGetUniformLocation(self.shader.program, f"light_positions[{i}]"), 1, glm.value_ptr(pos))
                GL.glUniform3fv(GL.glGetUniformLocation(self.shader.program, f"light_colors[{i}]"), 1, glm.value_ptr(color))
            GL.glUniform3fv(GL.glGetUniformLocation(self.shader.program, "cam_vec3"), 1, glm.value_ptr(renderer.camera.pos))

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
