# -*- coding: utf-8 -*-
"""
renderer module
===============
This module contains the `Renderer` class, which is responsible for everything related to rendering (including objects or movement).\n

It handles the GLFW window, the camera, and the scene. It also handles the input callbacks for the keyboard and mouse.
It is the main class of the application.
"""


# built-in imports
import typing
# pip imports
import glfw  # type: ignore
# local imports
from . import utils, Scene, Camera, FPSCamera


class Renderer:
    """
    The `Renderer` class is responsible for rendering the scene and handling input.\n

    What it does:
    - It initializes the camera and the scene.
    - It handles the input callbacks for the keyboard and mouse.
    - It updates the camera and scene matrices.
    - It renders the scene.
    - It cleans the resources when quitting.
    """
    def __init__(
            self: typing.Self,
            window: typing.Any,
            camera: type[Camera] = FPSCamera,
            /
            ) -> None:
        """
        Initializes the Renderer class.

        Parameters:
            window (typing.Any): The GLFW window.
            camera (type[camera.Camera]): The camera class to use. Defaults to `camera.FPSCamera`.
        """
        self.window = window
        self.camera = camera()
        self.scene = Scene()
        self.start = 0

        glfw.set_cursor_pos_callback(window, self.mouseCallback)
        glfw.set_scroll_callback(window, self.scrollCallback)

    def keyCallback(
            self: typing.Self,
            delta_time: float,
            /
            ) -> None:
        """
        Handles the keyboard input.\n

        It checks if the escape key is pressed and quits the application if it is.
        Else, it calls the camera's handleKeyboard method to handle the input.\n

        Parameters:
            delta_time (float): The time since the last frame.
        """
        if glfw.get_key(self.window, utils.KEY_BINDS.escape) == glfw.PRESS:
            self.quit()
            return

        self.camera.handleKeyboard(self.window, delta_time)

    def mouseCallback(
            self: typing.Self,
            win: typing.Any,
            mouse_x: float,
            mouse_y: float,
            /
            ) -> None:
        """
        Handles the mouse input.\n

        It calls the camera's handleMouse method to handle the input.\n

        Parameters:
            win (typing.Any): The GLFW window.
            mouse_x (float): The x position of the mouse.
            mouse_y (float): The y position of the mouse.
        """
        self.camera.handleMouse(mouse_x, mouse_y)

    def scrollCallback(
            self: typing.Self,
            win: typing.Any,
            delta_x: float,
            delta_y: float,
            /
            ) -> None:
        """
        Handles the scroll input.\n

        It calls the camera's handleScroll method to handle the input.\n

        Parameters:
            win (typing.Any): The GLFW window.
            delta_x (float): The x offset of the scroll.
            delta_y (float): The y offset of the scroll.
        """
        self.camera.handleScroll(delta_x, delta_y)

    def updateMatrices(
            self: typing.Self,
            /
            ) -> None:
        """
        Updates the camera and scene matrices.\n

        It calls the camera's updateMatrices method to update the view and projection matrices.
        It also calls the scene's updateModelMatrices method to update the model matrices of the objects in the scene.
        """
        self.camera.updateMatrices()
        self.scene.updateModelMatrices()

    def render(
            self: typing.Self,
            /
            ) -> None:
        """
        Renders the scene.\n

        It calls the scene's render method to render the objects in the scene.
        """
        self.scene.render(self.camera.view, self.camera.projection)

    def quit(
            self: typing.Self,
            /
            ) -> None:
        """
        Quits the application.\n

        It cleans the resources of the scene and sets the window to close.\n

        It should be called when the escape key is pressed.
        """
        self.scene.cleanRessources()
        glfw.set_window_should_close(self.window, True)
