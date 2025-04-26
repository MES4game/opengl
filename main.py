"""
main module
===========

Module to/that # TODO: set docstring

Functions
---------
- `initUser`
- `initWork`
- `loopWork`
- `main`
"""


# built-in imports
import os
import time
# pip imports
import glfw  # type: ignore
import OpenGL.GL as GL  # type: ignore
# local imports
import src


src.utils.ABS_PATH.root = os.path.dirname(os.path.abspath(__file__))
src.utils.ABS_PATH.updatePath()


def initUser() -> None:
    """
    Function to/that # TODO: set docstring

    Raises:
        # TODO: set exceptions
    """
    print("Press 'ESC' to exit.")
    print("Use 'W', 'A', 'S', 'D' to move.")
    print("Use 'Space'/'LShift' to move up/down.")
    print("Use Mouse to look around.")
    print("Use Mouse Wheel to zoom in/out.")
    print()


def initWork(
        renderer: src.Renderer,
        /
        ) -> None:
    """
    Function to/that # TODO: set docstring

    Args:
        renderer (`src.Renderer`): The renderer.
    Raises:
        # TODO: set exceptions
    """
    renderer.start = time.perf_counter_ns()
    # TODO


def loopWork(
        renderer: src.Renderer,
        delta_time: float,
        /
        ) -> None:
    """
    Function to/that # TODO: set docstring

    Args:
        renderer (`src.Renderer`): The renderer.
        delta_time (`float`): the time elapsed since last frame in seconds.
    Raises:
        # TODO: set exceptions
    """
    # TODO
    pass


def main() -> None:
    """
    Funtion to/that # TODO: set docstring

    Raises:
        # TODO: set exceptions
    """
    initUser()
    renderer: src.Renderer = src.Renderer()
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

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

        renderer.keyCallback(delta_time)

        loopWork(renderer, delta_time)

        renderer.updateMatrices()
        renderer.render()

        if last_reset > 0.5:
            fps = nb_frames / last_reset
            glfw.set_window_title(renderer.window, f"{src.utils.WINDOW_NAME} - Running at {fps:.1f} FPS")
            nb_frames = 0
            last_reset = 0.0
        else:
            nb_frames += 1
            last_reset += delta_time

        glfw.swap_buffers(renderer.window)
        glfw.poll_events()

    renderer.scene.cleanRessources()
    glfw.terminate()


if __name__ == "__main__":
    main()
