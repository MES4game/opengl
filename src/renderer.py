"""
renderer module
===============
Package: `src`

Module to/that # TODO: set docstring

Classes
-------
- `Renderer`
"""


# built-in imports
import collections.abc
import typing
# pip imports
import pyglm.glm as glm
import glfw  # type: ignore
import OpenGL.GL as GL  # type: ignore
# local imports
from . import utils, shapes, Scene, Camera, FPSCamera


class Renderer:
    """
    Renderer class
    ==============

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `keyCallback`
    - `mouseCallback`
    - `scrollCallback`
    - `updateMatrices`
    - `render`
    - `quit`
    """
    @staticmethod
    def initGlfw() -> typing.Any:
        """
        Method to/that # TODO: set docstring

        Returns:
            `typing.Any`: # TODO: set return
        Raises:
            # TODO: set exceptions
        """
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        window: typing.Any = glfw.create_window(utils.SCREEN_WIDTH, utils.SCREEN_HEIGHT, utils.WINDOW_NAME, None, None)

        if not window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        glfw.make_context_current(window)
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos(window, utils.SCREEN_WIDTH / 2, utils.SCREEN_HEIGHT / 2)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(*(utils.BACK_COLOR[:4]))

        print(
            f"OpenGL: {GL.glGetString(GL.GL_VERSION)},",
            f"GLSL: {GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)},",
            f"Renderer: {GL.glGetString(GL.GL_RENDERER)},",
            f"Vendor: {GL.glGetString(GL.GL_VENDOR)}"
        )

        return window

    def __init__(
            self: typing.Self,
            camera: type[Camera] = FPSCamera,
            /,
            *,
            game_handleKeyboard: collections.abc.Callable[[typing.Self, float], int] = lambda x, y: 0,
            game_handleMouse: collections.abc.Callable[[typing.Self, float, float], int] = lambda x, y, z: 0,
            game_handleScroll: collections.abc.Callable[[typing.Self, float, float], int] = lambda x, y, z: 0
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            camera (`type[Camera]`): the camera type to use. Default to `FPSCamera`.
            game_handleKeyboard (`collections.abc.Callable[[typing.Self, float], int]`): the function to call when a key is pressed.
            game_handleMouse (`collections.abc.Callable[[typing.Self, float, float], int]`): the function to call when the mouse is moved.
            game_handleScroll (`collections.abc.Callable[[typing.Self, float, float], int]`): the function to call when the scroll wheel is used.
        Raises:
            # TODO: set exceptions
        """
        self.window: typing.Any = Renderer.initGlfw()
        self.camera: Camera = camera(self.window)
        self.scene: Scene = Scene()
        self.skybox: shapes.Shape = shapes.Shape(shader_name="basic_tex", mesh_name="skybox", texture_name="skybox")
        self.skybox.setCoord(size=glm.vec3(utils.FAR - 0.000001))
        self.start: int = 0

        self.mouse_last_x: float = 0.0
        self.mouse_last_y: float = 0.0

        self.game_handleKeyboard: collections.abc.Callable[[typing.Self, float], int] = game_handleKeyboard
        self.game_handleMouse: collections.abc.Callable[[typing.Self, float, float], int] = game_handleMouse
        self.game_handleScroll: collections.abc.Callable[[typing.Self, float, float], int] = game_handleScroll
        glfw.set_cursor_pos_callback(self.window, self.mouseCallback)
        glfw.set_scroll_callback(self.window, self.scrollCallback)

    def keyCallback(
            self: typing.Self,
            delta_time: float,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta_time (`float`): the time elapsed since last frame in seconds.
        Raises:
            # TODO: set exceptions
        """
        if glfw.get_key(self.window, utils.KEY_BINDS.escape) == glfw.PRESS:
            self.quit()
            return

        if self.game_handleKeyboard(self, delta_time):
            return

        self.camera.handleKeyboard(delta_time)

    def mouseCallback(
            self: typing.Self,
            win: typing.Any,
            mouse_x: float,
            mouse_y: float,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            win (`typing.Any`): The GLFW window from wich the callback was called.
            mouse_x (`float`): The position of the mouse on x axis in the window.
            mouse_y (`float`): The position of the mouse on y axis in the window.
        Raises:
            # TODO: set exceptions
        """
        if self.game_handleMouse(self, mouse_x, mouse_y):
            return

        delta_x: float = (mouse_x - self.mouse_last_x)
        delta_y: float = (mouse_y - self.mouse_last_y)
        self.mouse_last_x = mouse_x
        self.mouse_last_y = mouse_y

        self.camera.handleMouse(delta_x, delta_y)

    def scrollCallback(
            self: typing.Self,
            win: typing.Any,
            delta_x: float,
            delta_y: float,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            win (`typing.Any`): The GLFW window from wich the callback was called.
            delta_x (`float`): The delta of the wheel on x axis in the window.
            delta_y (`float`): The delta of the wheel on y axis in the window.
        Raises:
            # TODO: set exceptions
        """
        if self.game_handleScroll(self, delta_x, delta_y):
            return

        self.camera.handleScroll(delta_x, delta_y)

    def updateMatrices(
            self: typing.Self,
            forced: bool = False,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            forced (`bool`): If we are forced to recalculate model matrices.
        Raises:
            # TODO: set exceptions
        """
        self.camera.updateMatrices(forced)
        self.scene.updateModelMatrix(forced)
        self.skybox.setCoord(pos=self.camera.pos)
        self.skybox.updateModelMatrix(forced)

    def render(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        self.scene.render(self.camera, self.camera.to_render)
        self.skybox.render(self.camera, self.camera.to_render)
        self.camera.to_render = False

    def quit(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        self.scene.cleanRessources()
        glfw.set_window_should_close(self.window, True)
