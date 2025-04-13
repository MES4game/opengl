# -*- coding: utf-8 -*-
"""
main module
===========
Here is the main program of the project.\n

It runs the main loop and calls the Renderer class to render the scene.
It also initializes GLFW and creates a window.\n

You can modify `initUser`, `initWork` and `loopWork` functions to customize the behavior of the program.
"""


# built-in imports
import os
import typing
import time
# pip imports
import numpy
import pyrr  # type: ignore
import glfw  # type: ignore
import OpenGL.GL as GL  # type: ignore
# local imports
import src


src.utils.ABS_PATH.root = os.path.dirname(os.path.abspath(__file__))
src.utils.ABS_PATH.updatePath()


def initUser() -> None:
    """
    Provides instructions for camera controls.
    Modify this function for every user interaction before glfw initialization.
    """
    print("Press 'ESC' to exit.")
    print("Use 'W', 'A', 'S', 'D' to move.")
    print("Use 'Space'/'LShift' to move up/down.")
    print("Use Mouse to look around.")
    print("Use Mouse Wheel to zoom in/out.")


def initGlfw() -> typing.Any:
    """
    Initializes GLFW and creates a window.

    Returns:
        window (typing.Any): The created GLFW window.
    """
    if not glfw.init():
        raise Exception("Failed to initialize GLFW")

    window: typing.Any = glfw.create_window(src.utils.SCREEN_WIDTH, src.utils.SCREEN_HEIGHT, src.utils.WINDOW_NAME, None, None)

    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)

    GL.glEnable(GL.GL_DEPTH_TEST)

    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos(window, src.utils.SCREEN_WIDTH / 2, src.utils.SCREEN_HEIGHT / 2)

    print(f"OpenGL {GL.glGetString(GL.GL_VERSION)}, GLSL {GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)}")
    print(f"Renderer {GL.glGetString(GL.GL_RENDERER)}, Vendor {GL.glGetString(GL.GL_VENDOR)}")

    return window


TSHAPES: tuple[type[src.shapes.Shape], ...] = (
    src.shapes.basics.Triangle,
    src.shapes.basics.Square,
    src.shapes.basics.Cube,
    src.shapes.basics.Pyramid,
    src.shapes.basics.Cone,
    src.shapes.basics.Cylinder,
    src.shapes.basics.Sphere
)


def initWork(
        renderer: src.Renderer,
        /
        ) -> None:
    """
    Function that is called after the initialization of everything and before the main loop.
    Modify this function to initialize everything like you want.\n

    Parameters:
        renderer (src.Renderer): The renderer instance.
    """
    renderer.start = time.perf_counter_ns()

    shapes: dict[str, src.shapes.Shape] = {}

    for i, tshape in enumerate(TSHAPES):
        shape = tshape()
        shapes[tshape.__name__] = shape

        theta = 2 * numpy.pi * i / len(TSHAPES)
        shape.setCoord(
            pos=pyrr.Vector3(
                [
                    numpy.cos(theta) * len(TSHAPES) / 2,
                    0.0,
                    numpy.sin(theta) * len(TSHAPES) / 2,
                ],
                dtype=numpy.single
            ),
            rot=pyrr.Vector3([0.0, 0.0, theta], dtype=numpy.single),
            size=pyrr.Vector3([1.0, 1.0, 1.0], dtype=numpy.single)
        )

    node = src.shapes.Node(shader_name="scene", mesh_name="cube")
    node.addElements(**shapes)

    renderer.scene.addElements(node=node, ground=src.shapes.basics.Square())
    renderer.scene.elements["ground"].setCoord(
        pos=pyrr.Vector3([0.0, -3.0, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([src.utils.FAR * 2, 1.0, src.utils.FAR * 2], dtype=numpy.single)
    )


def loopWork(
        renderer: src.Renderer,
        delta_time: float,
        /
        ) -> None:
    """
    Function that is called in the main loop.
    Modify this function to update everything like you want.\n

    Parameters:
        renderer (src.Renderer): The renderer instance.
        delta_time (float): The elapsed time since the last frame (in second).
    """
    node = renderer.scene.elements["node"]

    if not isinstance(node, src.shapes.Node):
        raise TypeError("Expected node to be of type src.shapes.Node")

    theta = 2 * numpy.pi * (time.perf_counter_ns() - renderer.start) / 2e10
    node.setCoord(
        pos=pyrr.Vector3(
            [
                numpy.cos(theta) * 10,
                0.0,
                numpy.sin(theta) * 10,
            ],
            dtype=numpy.single
        )
    )
    node.rotate(pyrr.Vector3([0.0, 0.0, delta_time], dtype=numpy.single))
    node.scale(pyrr.Vector3([1 + delta_time * 0.01] * 3, dtype=numpy.single))

    for i, tshape in enumerate(TSHAPES):
        element = node.children[tshape.__name__]
        element.setCoord(
            pos=pyrr.Vector3(
                [
                    element.pos[0],
                    (element.pos[1] + (delta_time if i // 3 else 0.0)) % 3.0,
                    element.pos[2]
                ],
                dtype=numpy.single
            ),
            size=pyrr.Vector3(
                [
                    max(0.25, (element.size[0] + (delta_time if i % 2 else 0.0)) % 3.0),
                    max(0.25, (element.size[1] + (delta_time if i % 2 else 0.0)) % 3.0),
                    max(0.25, (element.size[2] + (delta_time if i % 2 else 0.0)) % 3.0)
                ],
                dtype=numpy.single
            )
        )
        element.rotate(pyrr.Vector3(
            [
                delta_time if i % 3 == 2 else 0.0,
                delta_time if i % 3 == 1 else 0.0,
                delta_time if i % 3 == 0 else 0.0
            ],
            dtype=numpy.single
        ))


def main() -> None:
    """
    Main function to initialize GLFW, create a window and render using the Renderer class.
    """
    initUser()

    window: typing.Any = initGlfw()
    renderer: src.Renderer = src.Renderer(window)
    del window

    initWork(renderer)

    current_frame: int = time.perf_counter_ns()
    last_frame: int = current_frame
    delta_time: float = 0.0
    nb_frames: int = 0
    last_reset: float = 0.0
    fps: float = 1.0

    while not glfw.window_should_close(renderer.window):
        current_frame = time.perf_counter_ns()
        delta_time = (current_frame - last_frame) / 1e9
        last_frame = current_frame

        renderer.keyCallback(delta_time)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.5, 0.7, 1.0, 1.0)

        loopWork(renderer, delta_time)

        renderer.updateMatrices()
        renderer.render()

        if last_reset > 1.0:
            fps = nb_frames / last_reset
            glfw.set_window_title(renderer.window, f"{src.utils.WINDOW_NAME} - Running at {fps:.1f} FPS")
            nb_frames = 0
            last_reset = 0.0
        else:
            nb_frames += 1
            last_reset += delta_time

        glfw.swap_buffers(renderer.window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
