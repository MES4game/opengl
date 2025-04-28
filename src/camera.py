"""
camera module
=============
Package: `src`

Module to/that # TODO: set docstring

Classes
-------
- `Camera`
- `FPSCamera`
- `FreeCamera`
- `OrbitCamera`
- `TPSCamera`
"""


# built-in imports
import typing
import math
# pip imports
import pyglm.glm as glm
import glfw  # type: ignore
# local imports
from . import utils


class Camera:
    """
    Camera class
    ============

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
    - `updateVectors`
    - `updateMatrices`
    - `handleKeyboard`
    - `handleMouse`
    - `handleScroll`
    """
    __angles: list[float | None] = [
        None,
        0.0,
        math.pi,
        None,
        -math.pi / 2,
        -math.pi / 4,
        -math.pi * 3 / 4,
        -math.pi / 2,
        math.pi / 2,
        math.pi / 4,
        math.pi * 3 / 4,
        math.pi / 2,
        None,
        0.0,
        math.pi,
        None,
    ]

    def __init__(
            self: typing.Self,
            window: typing.Any,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            window (`typing.Any`): the GLFW window where we are.
        Raises:
            # TODO: set exceptions
        """
        self.window: typing.Any = window

        self.pos: glm.vec3 = glm.vec3(0, utils.PLAYER_SIZE * 0.95, 0)
        self.yaw: float = 0.0
        self.pitch: float = 0.0
        self.fov: float = math.pi / 4

        self.front: glm.vec3 = glm.vec3(1, 0, 0)
        self.right: glm.vec3 = glm.vec3(0, 0, 1)
        self.up: glm.vec3 = glm.vec3(0, 1, 0)
        self.world_up: glm.vec3 = glm.vec3(0, 1, 0)

        self.view: glm.mat4x4 = glm.mat4x4()
        self.proj: glm.mat4x4 = glm.mat4x4()

        self.mouse_last_x, self.mouse_last_y = glfw.get_cursor_pos(self.window)

        self.view_to_update: bool = True
        self.proj_to_update: bool = True
        self.to_render: bool = True

        self.updateVectors()
        self.updateMatrices()

    def updateVectors(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Raises:
            # TODO: set exceptions
        """
        pitch_cos: float = math.cos(self.pitch)
        self.front = glm.vec3(
            math.cos(self.yaw) * pitch_cos,
            math.sin(self.pitch),
            math.sin(self.yaw) * pitch_cos
        )
        # TODO: do normalize by myself (because front and world_up are already normalized)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))

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
        if self.view_to_update or forced:
            self.view = glm.lookAt(
                self.pos,
                self.pos + self.front,
                self.up
            )
            self.view_to_update = False
            self.to_render = True

        if self.proj_to_update or forced:
            self.proj = glm.perspective(
                self.fov,
                utils.SCREEN_WIDTH / utils.SCREEN_HEIGHT,
                utils.NEAR,
                utils.FAR
            )
            self.proj_to_update = False
            self.to_render = True

    def handleKeyboard(
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
        velocity: float = utils.MOVE_SPEED * delta_time

        combo: int = 0
        if glfw.get_key(self.window, utils.KEY_BINDS.move_forward) == glfw.PRESS:
            combo += 1
        if glfw.get_key(self.window, utils.KEY_BINDS.move_backward) == glfw.PRESS:
            combo += 2
        if glfw.get_key(self.window, utils.KEY_BINDS.move_left) == glfw.PRESS:
            combo += 4
        if glfw.get_key(self.window, utils.KEY_BINDS.move_right) == glfw.PRESS:
            combo += 8

        move_rot: float | None = Camera.__angles[combo]
        if move_rot is not None:
            direction: float = self.yaw + move_rot
            move_pos: glm.vec3 = glm.vec3(
                math.cos(direction) * velocity,
                0,
                math.sin(direction) * velocity
            )
            self.pos += move_pos

        if glfw.get_key(self.window, utils.KEY_BINDS.jump) == glfw.PRESS and glfw.get_key(self.window, utils.KEY_BINDS.sneak) == glfw.PRESS:
            pass
        elif glfw.get_key(self.window, utils.KEY_BINDS.jump) == glfw.PRESS:
            self.pos += self.world_up * utils.FLY_JUMP_HEIGHT * delta_time
        elif glfw.get_key(self.window, utils.KEY_BINDS.sneak) == glfw.PRESS:
            self.pos -= self.world_up * utils.FLY_SNEAK_HEIGHT * delta_time

        self.pos = glm.clamp(self.pos, -utils.BORDER, utils.BORDER)
        self.view_to_update = True

    def handleMouse(
            self: typing.Self,
            delta_x: float,
            delta_y: float,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta_x (`float`): The delta position of the mouse on x axis.
            delta_y (`float`): The delta position of the mouse on y axis.
        Raises:
            # TODO: set exceptions
        """
        self.yaw += delta_x * utils.CAM_SPEED
        self.yaw = self.yaw % utils.TWO_PI

        self.pitch += delta_y * utils.CAM_SPEED
        self.pitch = max(utils.MIN_CAM_PITCH, min(utils.MAX_CAM_PITCH, self.pitch))

        self.updateVectors()
        self.view_to_update = True

    def handleScroll(
            self: typing.Self,
            delta_x: float,
            delta_y: float,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            delta_x (`float`): The delta of the wheel on x axis.
            delta_y (`float`): The delta of the wheel on y axis.
        Raises:
            # TODO: set exceptions
        """
        self.fov -= delta_y * utils.ZOOM_SPEED
        self.fov = max(utils.MIN_ZOOM, min(utils.MAX_ZOOM, self.fov))
        self.proj_to_update = True


class FPSCamera(Camera):
    """
    FPSCamera class
    ===============
    Parent class: `Camera`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    @typing.override
    def __init__(
            self: typing.Self,
            window: typing.Any,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            window (`typing.Any`): the GLFW window where we are.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(window)
        # TODO


class FreeCamera(Camera):
    """
    FreeCamera class
    ================
    Parent class: `Camera`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    @typing.override
    def __init__(
            self: typing.Self,
            window: typing.Any,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            window (`typing.Any`): the GLFW window where we are.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(window)
        # TODO


class OrbitCamera(Camera):
    """
    OrbitCamera class
    =================
    Parent class: `Camera`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    @typing.override
    def __init__(
            self: typing.Self,
            window: typing.Any,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            window (`typing.Any`): the GLFW window where we are.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(window)
        # TODO


class TPSCamera(Camera):
    """
    TPSCamera class
    ===============
    Parent class: `Camera`

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    """
    @typing.override
    def __init__(
            self: typing.Self,
            window: typing.Any,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            window (`typing.Any`): the GLFW window where we are.
        Raises:
            # TODO: set exceptions
        """
        super().__init__(window)
        # TODO
