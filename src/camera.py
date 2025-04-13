# -*- coding: utf-8 -*-
"""
camera module
=============
This module contains the `Camera` class and its subclasses.\n

The `Camera` class is used to represent a camera in 3D space.\n

All the subclasses of `Camera` are used to represent different types of cameras:
- `FPSCamera`: First Person Shooter camera.
- `FreeCamera`: Free camera that can move freely in 3D space (also called no-clip).
- `OrbitCamera`: Camera that orbits around a target.
- `TPSCamera`: Third Person Shooter camera.
"""


# built-in imports
import typing
# pip imports
import numpy
import pyrr  # type: ignore
import glfw  # type: ignore
# local imports
from . import utils


class Camera:
    """
    Represents a camera in 3D space.\n

    The camera is defined by its position, orientation (yaw and pitch), field of view (fov), and the vectors that define its orientation (front, right, up).
    The camera can be moved and rotated using keyboard and mouse inputs.
    """
    __angles: list[float | None] = [
        None,
        0.0,
        numpy.pi,
        None,
        -numpy.pi / 2,
        -numpy.pi / 4,
        -numpy.pi * 3 / 4,
        -numpy.pi / 2,
        numpy.pi / 2,
        numpy.pi / 4,
        numpy.pi * 3 / 4,
        numpy.pi / 2,
        None,
        0.0,
        numpy.pi,
        None,
    ]

    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Initializes the `Camera` object.\n

        The camera is initialized with the following parameters:
        - `pos`: The position of the camera in 3D space.
        - `yaw`: The yaw angle of the camera in degrees (in french we say theta).
        - `pitch`: The pitch angle of the camera in degrees (in french we say phi).
        - `fov`: The field of view of the camera in degrees.
        - `front`: The front vector of the camera.
        - `right`: The right vector of the camera.
        - `up`: The up vector of the camera.
        - `world_up`: The world up vector.
        - `mouse_last_x`: The last x-axis position of the mouse.
        - `mouse_last_y`: The last y-axis position of the mouse.
        - `view_updated`: A boolean to check if the view matrix needs to be updated.
        - `projection_updated`: A boolean to check if the projection matrix needs to be updated.
        """
        self.pos = pyrr.Vector3([0, utils.PLAYER_SIZE, 0], dtype=numpy.single)
        self.yaw = 0.0
        self.pitch = 0.0
        self.fov = 45.0

        self.front = pyrr.Vector3([1, 0, 0], dtype=numpy.single)
        self.right = pyrr.Vector3([0, 0, -1], dtype=numpy.single)
        self.up = pyrr.Vector3([0, 1, 0], dtype=numpy.single)
        self.world_up = pyrr.Vector3([0, 1, 0], dtype=numpy.single)

        self.mouse_last_x = 0.0
        self.mouse_last_y = 0.0

        self.view_updated = True
        self.projection_updated = True

        self.updateVectors()
        self.updateMatrices()

    def updateVectors(
            self: typing.Self,
            /
            ) -> None:
        """
        Updates the front, right and up vectors of the camera based on the yaw and pitch angles.\n

        The front vector is calculated using the yaw and pitch angles.
        The right vector is calculated using the cross product of the front and world up vectors.
        The up vector is calculated using the cross product of the right and front vectors.
        """
        front = pyrr.Vector3([
            numpy.cos(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch)),
            numpy.sin(numpy.radians(self.pitch)),
            numpy.sin(numpy.radians(self.yaw)) * numpy.cos(numpy.radians(self.pitch))
        ])
        self.front = front.normalized
        self.right = self.front.cross(self.world_up).normalized
        self.up = self.right.cross(self.front).normalized

    def updateMatrices(
            self: typing.Self,
            /
            ) -> None:
        """
        Updates the view and projection matrices of the camera.
        """
        if self.view_updated:
            self.view = pyrr.Matrix44.look_at(
                eye=self.pos,
                target=self.pos + self.front,
                up=self.up,
                dtype=numpy.single
            )
            self.view_updated = False

        if self.projection_updated:
            self.projection = pyrr.Matrix44.perspective_projection(
                fovy=self.fov,
                aspect=utils.SCREEN_WIDTH / utils.SCREEN_HEIGHT,
                near=utils.NEAR,
                far=utils.FAR,
                dtype=numpy.single
            )
            self.projection_updated = False

    def handleKeyboard(
            self: typing.Self,
            window: typing.Any,
            delta_time: float,
            /
            ) -> None:
        """
        Handles the keyboard event to move the camera.
        The movement is limited to the border defined by `utils.BORDER`.
        The movement is applied to the position of the camera.\n

        The movement is based on the key binds defined in `utils.KEY_BINDS` and using corresponding angles from `cls.__angles`.\n

        And the movement is based on the velocity defined by `utils.MOVE_SPEED`.
        The movement is based on the delta time to make it frame rate independent.\n

        Parameters:
            window (typing.Any): The window object.
            delta_time (float): The delta time since the last frame.
        """
        velocity = utils.MOVE_SPEED * delta_time

        combo: int = 0
        if glfw.get_key(window, utils.KEY_BINDS.move_forward) == glfw.PRESS:
            combo += 1
        if glfw.get_key(window, utils.KEY_BINDS.move_backward) == glfw.PRESS:
            combo += 2
        if glfw.get_key(window, utils.KEY_BINDS.move_left) == glfw.PRESS:
            combo += 4
        if glfw.get_key(window, utils.KEY_BINDS.move_right) == glfw.PRESS:
            combo += 8

        move_rot: float | None = self.__class__.__angles[combo]
        if move_rot is not None:
            direction: float = (self.yaw * numpy.pi / 180) + move_rot
            move_pos: pyrr.Vector3 = pyrr.Vector3([
                numpy.cos(direction) * velocity,
                0.0,
                numpy.sin(direction) * velocity
            ], dtype=numpy.single)
            self.pos += move_pos

        if glfw.get_key(window, utils.KEY_BINDS.jump) == glfw.PRESS and glfw.get_key(window, utils.KEY_BINDS.sneak) == glfw.PRESS:
            pass
        elif glfw.get_key(window, utils.KEY_BINDS.jump) == glfw.PRESS:
            self.pos += self.world_up * velocity
        elif glfw.get_key(window, utils.KEY_BINDS.sneak) == glfw.PRESS:
            self.pos -= self.world_up * velocity

        self.pos = pyrr.Vector3(numpy.clip(self.pos, -utils.BORDER, utils.BORDER), dtype=numpy.single)
        self.view_updated = True

    def handleMouse(
            self: typing.Self,
            mouse_x: float,
            mouse_y: float,
            /
            ) -> None:
        """
        Handles the mouse event to rotate the camera.
        The rotation is limited to a minimum and maximum value.
        The rotation is applied to the yaw and pitch of the camera.\n

        Parameters:
            mouse_x (float): The x-axis position of the mouse.
            mouse_y (float): The y-axis position of the mouse.
        """
        delta_x = (mouse_x - self.mouse_last_x) * utils.CURSOR_SPEED
        delta_y = (self.mouse_last_y - mouse_y) * utils.CURSOR_SPEED

        self.mouse_last_x = mouse_x
        self.mouse_last_y = mouse_y

        self.yaw += delta_x
        self.pitch += delta_y

        self.yaw = numpy.fmod(self.yaw, 360.0)
        self.pitch = max(-89.0, min(89.0, self.pitch))

        self.view_updated = True

        self.updateVectors()

    def handleScroll(
            self: typing.Self,
            delta_x: float,
            delta_y: float,
            /
            ) -> None:
        """
        Handles the scroll event to zoom in and out.
        The zoom is limited to a minimum and maximum value.
        The zoom is applied to the field of view (fov) of the camera.\n

        Parameters:
            delta_x (float): The x-axis scroll value.
            delta_y (float): The y-axis scroll value.
        """
        self.fov -= delta_y * utils.ZOOM_SPEED
        self.fov = max(utils.MIN_ZOOM, min(utils.MAX_ZOOM, self.fov))
        self.projection_updated = True


class FPSCamera(Camera):
    """
    Parent class: `Camera`\n

    # TODO
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        # TODO
        """
        super().__init__()
        # TODO


class FreeCamera(Camera):
    """
    Parent class: `Camera`\n

    # TODO
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        # TODO
        """
        super().__init__()
        # TODO


class OrbitCamera(Camera):
    """
    Parent class: `Camera`\n

    # TODO
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        # TODO
        """
        super().__init__()
        # TODO


class TPSCamera(Camera):
    """
    Parent class: `Camera`\n

    # TODO
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        # TODO
        """
        super().__init__()
        # TODO
