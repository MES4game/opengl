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

    human_node = src.shapes.Node()

    # Torse et Tête

    torse = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    torse.setCoord(
        pos=pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single),
        rot=pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([src.utils.PLAYER_SIZE * 2 / 3, src.utils.PLAYER_SIZE, src.utils.PLAYER_SIZE * 5 / 12], dtype=numpy.single)
    )
    human_node.addElements(torse=torse)

    tete = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    tete.setCoord(
        pos=pyrr.Vector3([0.0, 1.425, 0.0], dtype=numpy.single),
        rot=pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.6, 0.5, 0.7], dtype=numpy.single)
    )
    torse.addElements(tete=tete)

    cou = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cou.setCoord(
        pos=pyrr.Vector3([0.0, 0.9, 0.0], dtype=numpy.single),
        rot=pyrr.Vector3([0.0, 0.0, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.3, 0.3, 0.5], dtype=numpy.single)
    )
    torse.addElements(cou=cou)

    bassin = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bassin.setCoord(
        pos=pyrr.Vector3([0.0, -0.75, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.2, 1.1], dtype=numpy.single)
    )
    torse.addElements(bassin=bassin)

    # Bras Gauche

    epaule_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    epaule_gauche.setCoord(
        pos=pyrr.Vector3([-0.75, 0.75, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.4, 0.25, 0.7], dtype=numpy.single)
    )
    torse.addElements(epaule_gauche=epaule_gauche)

    bras_haut_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_haut_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.6, 1.5, 0.6], dtype=numpy.single)
    )
    epaule_gauche.addElements(bras_haut_gauche=bras_haut_gauche)

    coude_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    coude_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.4, 1.1], dtype=numpy.single)
    )
    bras_haut_gauche.addElements(coude_gauche=coude_gauche)

    bras_bas_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_bas_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.9, 2.5, 0.9], dtype=numpy.single)
    )
    coude_gauche.addElements(bras_bas_gauche=bras_bas_gauche)

    main_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    main_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.75, 0.75, 0.75], dtype=numpy.single)
    )
    bras_bas_gauche.addElements(main_gauche=main_gauche)

    # Bras Droit

    epaule_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    epaule_droite.setCoord(
        pos=pyrr.Vector3([0.75, 0.75, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.4, 0.25, 0.7], dtype=numpy.single)
    )
    torse.addElements(epaule_droite=epaule_droite)

    bras_haut_droit = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_haut_droit.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.6, 1.5, 0.6], dtype=numpy.single)
    )
    epaule_droite.addElements(bras_haut_droit=bras_haut_droit)

    coude_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    coude_droit.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.4, 1.1], dtype=numpy.single)
    )
    bras_haut_droit.addElements(coude_droit=coude_droit)

    bras_bas_droit = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_bas_droit.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.9, 2.5, 0.9], dtype=numpy.single)
    )
    coude_droit.addElements(bras_bas_droit=bras_bas_droit)

    main_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    main_droite.setCoord(
        pos=pyrr.Vector3([0.0, -0.3, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.75, 0.75, 0.75], dtype=numpy.single)
    )
    bras_bas_droit.addElements(main_droite=main_droite)

    # Jambe Gauche

    hanche_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    hanche_gauche.setCoord(
        pos=pyrr.Vector3([-0.45, -0.15, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.4, 1.5, 0.8], dtype=numpy.single)
    )
    bassin.addElements(hanche_gauche=hanche_gauche)

    cuisse_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cuisse_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.6, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.7, 1.6, 0.6], dtype=numpy.single)
    )
    hanche_gauche.addElements(cuisse_gauche=cuisse_gauche)

    genou_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    genou_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.5, 1.1], dtype=numpy.single)
    )
    cuisse_gauche.addElements(genou_gauche=genou_gauche)

    jambe_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    jambe_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.95, 2.0, 0.95], dtype=numpy.single)
    )
    genou_gauche.addElements(jambe_gauche=jambe_gauche)

    cheville_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    cheville_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.3, 1.1], dtype=numpy.single)
    )
    jambe_gauche.addElements(cheville_gauche=cheville_gauche)

    pied_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    pied_gauche.setCoord(
        pos=pyrr.Vector3([0.0, -0.15, 0.15], dtype=numpy.single),
        size=pyrr.Vector3([1.0, 1.0, 1.5], dtype=numpy.single)
    )
    cheville_gauche.addElements(pied_gauche=pied_gauche)

    # Jambe Droite

    hanche_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    hanche_droite.setCoord(
        pos=pyrr.Vector3([0.45, -0.15, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.4, 1.5, 0.8], dtype=numpy.single)
    )
    bassin.addElements(hanche_droite=hanche_droite)

    cuisse_droite = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cuisse_droite.setCoord(
        pos=pyrr.Vector3([0.0, -0.6, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.7, 1.6, 0.6], dtype=numpy.single)
    )
    hanche_droite.addElements(cuisse_droite=cuisse_droite)

    genou_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    genou_droit.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.5, 1.1], dtype=numpy.single)
    )
    cuisse_droite.addElements(genou_droit=genou_droit)

    jambe_droite = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    jambe_droite.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([0.95, 2.0, 0.95], dtype=numpy.single)
    )
    genou_droit.addElements(jambe_droite=jambe_droite)

    cheville_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    cheville_droite.setCoord(
        pos=pyrr.Vector3([0.0, -0.45, 0.0], dtype=numpy.single),
        size=pyrr.Vector3([1.1, 0.3, 1.1], dtype=numpy.single)
    )
    jambe_droite.addElements(cheville_droite=cheville_droite)

    pied_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    pied_droit.setCoord(
        pos=pyrr.Vector3([0.0, -0.15, 0.15], dtype=numpy.single),
        size=pyrr.Vector3([1.0, 1.0, 1.5], dtype=numpy.single)
    )
    cheville_droite.addElements(pied_droit=pied_droit)

    # Rotation des bras
    epaule_gauche.rotate(pyrr.Vector3([0.0, -numpy.pi / 2, 0.0], dtype=numpy.single))
    epaule_droite.rotate(pyrr.Vector3([0.0, numpy.pi / 2, 0.0], dtype=numpy.single))

    # Humain via .obj file
    human_shape = src.shapes.Shape(shader_name="scene", mesh_name="human")

    human_shape.move(pyrr.Vector3([0.0, -0.5, 2.5], dtype=numpy.single))
    human_shape.rotate(pyrr.Vector3([0.0, 0.0, numpy.pi], dtype=numpy.single))
    human_shape.scale(pyrr.Vector3([src.utils.PLAYER_SIZE * 0.9] * 3, dtype=numpy.single))
    human_node.move(pyrr.Vector3([0.0, 0.0, -2.5], dtype=numpy.single))

    humans = src.shapes.Node()
    humans.addElements(human_shape=human_shape, human_node=human_node)
    renderer.scene.addElements(humans=humans)


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
    # TODO
    pass


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
