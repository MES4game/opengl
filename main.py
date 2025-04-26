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
import math
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

    human_node = src.shapes.Node()

    # Torse et Tête

    torse = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    torse.setCoord(
        pos=glm.vec3(),
        rot=glm.vec3(),
        size=glm.vec3(src.utils.PLAYER_SIZE * 2 / 3, src.utils.PLAYER_SIZE, src.utils.PLAYER_SIZE * 5 / 12)
    )
    human_node.addElements(torse=torse)

    tete = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    tete.setCoord(
        pos=glm.vec3(0, 1.425, 0),
        size=glm.vec3(0.6, 0.5, 0.7)
    )
    torse.addElements(tete=tete)

    cou = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cou.setCoord(
        pos=glm.vec3(0, 0.9, 0),
        size=glm.vec3(0.3, 0.3, 0.5)
    )
    torse.addElements(cou=cou)

    bassin = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bassin.setCoord(
        pos=glm.vec3(0, -0.75, 0),
        size=glm.vec3(1.1, 0.2, 1.1)
    )
    torse.addElements(bassin=bassin)

    # Bras Gauche

    epaule_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    epaule_gauche.setCoord(
        pos=glm.vec3(-0.75, 0.75, 0),
        size=glm.vec3(0.4, 0.25, 0.7)
    )
    torse.addElements(epaule_gauche=epaule_gauche)

    bras_haut_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_haut_gauche.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(0.6, 1.5, 0.6)
    )
    epaule_gauche.addElements(bras_haut_gauche=bras_haut_gauche)

    coude_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    coude_gauche.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(1.1, 0.4, 1.1)
    )
    bras_haut_gauche.addElements(coude_gauche=coude_gauche)

    bras_bas_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_bas_gauche.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(0.9, 2.5, 0.9)
    )
    coude_gauche.addElements(bras_bas_gauche=bras_bas_gauche)

    main_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    main_gauche.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(0.75, 0.75, 0.75)
    )
    bras_bas_gauche.addElements(main_gauche=main_gauche)

    # Bras Droit

    epaule_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    epaule_droite.setCoord(
        pos=glm.vec3(0.75, 0.75, 0),
        size=glm.vec3(0.4, 0.25, 0.7)
    )
    torse.addElements(epaule_droite=epaule_droite)

    bras_haut_droit = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_haut_droit.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(0.6, 1.5, 0.6)
    )
    epaule_droite.addElements(bras_haut_droit=bras_haut_droit)

    coude_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    coude_droit.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(1.1, 0.4, 1.1)
    )
    bras_haut_droit.addElements(coude_droit=coude_droit)

    bras_bas_droit = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    bras_bas_droit.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(0.9, 2.5, 0.9)
    )
    coude_droit.addElements(bras_bas_droit=bras_bas_droit)

    main_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    main_droite.setCoord(
        pos=glm.vec3(0, -0.3, 0),
        size=glm.vec3(0.75, 0.75, 0.75)
    )
    bras_bas_droit.addElements(main_droite=main_droite)

    # Jambe Gauche

    hanche_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    hanche_gauche.setCoord(
        pos=glm.vec3(-0.45, -0.15, 0),
        size=glm.vec3(0.4, 1.5, 0.8)
    )
    bassin.addElements(hanche_gauche=hanche_gauche)

    cuisse_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cuisse_gauche.setCoord(
        pos=glm.vec3(0, -0.6, 0),
        size=glm.vec3(0.7, 1.6, 0.6)
    )
    hanche_gauche.addElements(cuisse_gauche=cuisse_gauche)

    genou_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    genou_gauche.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(1.1, 0.5, 1.1)
    )
    cuisse_gauche.addElements(genou_gauche=genou_gauche)

    jambe_gauche = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    jambe_gauche.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(0.95, 2, 0.95)
    )
    genou_gauche.addElements(jambe_gauche=jambe_gauche)

    cheville_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    cheville_gauche.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(1.1, 0.3, 1.1)
    )
    jambe_gauche.addElements(cheville_gauche=cheville_gauche)

    pied_gauche = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    pied_gauche.setCoord(
        pos=glm.vec3(0, -0.15, 0.15),
        size=glm.vec3(1, 1, 1.5)
    )
    cheville_gauche.addElements(pied_gauche=pied_gauche)

    # Jambe Droite

    hanche_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    hanche_droite.setCoord(
        pos=glm.vec3(0.45, -0.15, 0),
        size=glm.vec3(0.4, 1.5, 0.8)
    )
    bassin.addElements(hanche_droite=hanche_droite)

    cuisse_droite = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    cuisse_droite.setCoord(
        pos=glm.vec3(0, -0.6, 0),
        size=glm.vec3(0.7, 1.6, 0.6)
    )
    hanche_droite.addElements(cuisse_droite=cuisse_droite)

    genou_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    genou_droit.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(1.1, 0.5, 1.1)
    )
    cuisse_droite.addElements(genou_droit=genou_droit)

    jambe_droite = src.shapes.Node(shader_name="scene", mesh_name="cylinder")
    jambe_droite.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(0.95, 2, 0.95)
    )
    genou_droit.addElements(jambe_droite=jambe_droite)

    cheville_droite = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    cheville_droite.setCoord(
        pos=glm.vec3(0, -0.45, 0),
        size=glm.vec3(1.1, 0.3, 1.1)
    )
    jambe_droite.addElements(cheville_droite=cheville_droite)

    pied_droit = src.shapes.Node(shader_name="scene", mesh_name="sphere")
    pied_droit.setCoord(
        pos=glm.vec3(0, -0.15, 0.15),
        size=glm.vec3(1, 1, 1.5)
    )
    cheville_droite.addElements(pied_droit=pied_droit)

    # Rotation des bras
    epaule_gauche.rotate(glm.vec3(0, -math.pi * 2 / 3, 0))
    epaule_droite.rotate(glm.vec3(0, math.pi * 2 / 3, 0))
    hanche_gauche.rotate(glm.vec3(0, -math.pi / 6, 0))
    hanche_droite.rotate(glm.vec3(0, math.pi / 6, 0))

    # Humain via .obj file
    human_shape = src.shapes.Shape(shader_name="scene", mesh_name="human")
    human_shape.scale(glm.vec3(src.utils.PLAYER_SIZE * 0.9))

    humans = src.shapes.Node()
    humans.addElements(human_shape=human_shape, human_node=human_node)
    renderer.scene.addElements(humans=humans)


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
    humans = renderer.scene.children["humans"]

    if not isinstance(humans, src.shapes.Node):
        raise TypeError("humans is not a Node")

    elapsed = (time.perf_counter_ns() - renderer.start) / 1e9

    humans.children["human_node"].setCoord(
        pos=glm.vec3(2.5 * math.cos(elapsed), 0, 2.5 * math.sin(elapsed)),
        rot=glm.vec3(-elapsed - math.pi / 2, 0, 0)
    )

    humans.children["human_shape"].setCoord(
        pos=glm.vec3(2.5 * math.cos(elapsed + math.pi), -0.5, 2.5 * math.sin(elapsed + math.pi)),
        rot=glm.vec3(-elapsed + math.pi / 2, 0, 0)
    )


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
