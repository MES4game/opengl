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
import pyglm.glm as glm
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

    cube_cia = src.shapes.basics.Cube(texture_name="logo_cia_2048")
    cube_cia.move(glm.vec3(0, 3, 0))
    sphere_cia = src.shapes.basics.Sphere(texture_name="logo_cia_2048")
    sphere_cia.move(glm.vec3(0, -3, 0))

    cube_tex = src.shapes.basics.Cube(texture_name="diamond")
    cube_light = src.shapes.basics.Cube(color=glm.vec3(0.4, 0.9, 0.8), has_light=True)
    cube_texlight = src.shapes.basics.Cube(texture_name="diamond", has_light=True)
    cube_tex.move(glm.vec3(0, 0, -3))
    cube_light.move(glm.vec3(0, 0, 0))
    cube_texlight.move(glm.vec3(0, 0, 3))

    pyramid_tex = src.shapes.basics.Pyramid(texture_name="diamond")
    pyramid_light = src.shapes.basics.Pyramid(color=glm.vec3(0.4, 0.9, 0.8), has_light=True)
    pyramid_texlight = src.shapes.basics.Pyramid(texture_name="diamond", has_light=True)
    pyramid_tex.move(glm.vec3(3, 0, -3))
    pyramid_light.move(glm.vec3(3, 0, 0))
    pyramid_texlight.move(glm.vec3(3, 0, 3))

    cylinder_tex = src.shapes.basics.Cylinder(texture_name="diamond")
    cylinder_light = src.shapes.basics.Cylinder(color=glm.vec3(0.4, 0.9, 0.8), has_light=True)
    cylinder_texlight = src.shapes.basics.Cylinder(texture_name="diamond", has_light=True)
    cylinder_tex.move(glm.vec3(-3, 0, -3))
    cylinder_light.move(glm.vec3(-3, 0, 0))
    cylinder_texlight.move(glm.vec3(-3, 0, 3))

    renderer.scene.addElements(
        cube_tex,
        cube_light,
        cube_texlight,
        pyramid_tex,
        pyramid_light,
        pyramid_texlight,
        cylinder_tex,
        cylinder_light,
        cylinder_texlight,
        cube_cia=cube_cia,
        sphere_cia=sphere_cia
    )


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
    for child in renderer.scene.children.values():
        child.rotate(glm.vec3(delta_time, 0, 0))

    renderer.scene.children["cube_cia"].rotate(glm.vec3(0, delta_time, delta_time))
    renderer.scene.children["sphere_cia"].rotate(glm.vec3(0, delta_time, delta_time))


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
