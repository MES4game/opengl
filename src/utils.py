# -*- coding: utf-8 -*-
"""
utils module
============
This module contains utility globals, functions and classes for the project.\n

It is used to manage paths, extensions, key bindings and other constants.\n

Here are the classes of this module:
- RelPath: This class contains the relative paths of the project.
- AbsPath: This class contains the absolute paths of the project.
- Extensions: This class contains the extensions for the files used in the project.
- KeyBinds: This class contains the key bindings for the project.

Here are the global variables of this module:
- REL_PATH: This variable contains the relative paths of the project.
- ABS_PATH: This variable contains the absolute paths of the project.
- EXTENSIONS: This variable contains the extensions for the files used in the project.
- WINDOW_NAME: This variable contains the name of the window.
- SCREEN_WIDTH: This variable contains the width of the window.
- SCREEN_HEIGHT: This variable contains the height of the window.
- NEAR: This variable contains the near plane distance.
- FAR: This variable contains the far plane distance.
- BORDER: This variable contains the border of the map.
- PLAYER_SIZE: This variable contains the size of the player.
- CURSOR_SPEED: This variable contains the speed of the cursor (mouse).
- ZOOM_SPEED: This variable contains the speed of the zoom (fov).
- MIN_ZOOM: This variable contains the minimum zoom (fov).
- MAX_ZOOM: This variable contains the maximum zoom (fov).
- MOVE_SPEED: This variable contains the speed of the player.
- JUMP_HEIGHT: This variable contains the height of the jump.
- SNEAK_HEIGHT: This variable contains the height of the sneak.
- KEY_DICT: This variable contains the keys for the project.
- KEY_BINDS: This variable contains the key bindings for the project.
"""


# built-in imports
import os
import typing
import dataclasses
# pip imports
import glfw  # type: ignore
# local imports


@dataclasses.dataclass
class RelPath:
    """
    This class contains the relative paths of the project.
    It is used to manage the paths of the project.\n

    It contains the following attributes:
    - src: This attribute contains the name of the src folder (in root).
    - assets: This attribute contains the name of the assets folder (in root).
    - shaders: This attribute contains the name of the shaders folder (in assets).
    - meshes: This attribute contains the name of the meshes folder (in assets).
    - materials: This attribute contains the name of the materials folder (in assets).
    - textures: This attribute contains the name of the textures folder (in assets).
    """
    src: str = "src"
    assets: str = "assets"
    shaders: str = "shaders"
    meshes: str = "meshes"
    materials: str = "materials"
    textures: str = "textures"


@dataclasses.dataclass
class AbsPath:
    """
    This class contains the absolute paths of the project.
    It is used to manage the paths of the project.\n

    It contains the following attributes:
    - root: This attribute contains the root path of the project.
    - src: This attribute contains the absolute path of the src folder.
    - shaders: This attribute contains the absolute path of the shaders folder.
    - meshes: This attribute contains the absolute path of the meshes folder.
    - materials: This attribute contains the absolute path of the materials folder.
    - textures: This attribute contains the absolute path of the textures folder.
    """
    root: str = os.path.dirname(os.path.abspath(__file__))
    src: str = ""
    shaders: str = ""
    meshes: str = ""
    materials: str = ""
    textures: str = ""

    def __post_init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Build the absolute paths of the project.
        This function is called after the object is created.
        """
        self.updatePath()

    def updatePath(
            self: typing.Self,
            /
            ) -> None:
        """
        Update the absolute paths of the project.
        """
        self.src = os.path.join(self.root, REL_PATH.src)
        self.shaders = os.path.join(self.root, REL_PATH.assets, REL_PATH.shaders)
        self.meshes = os.path.join(self.root, REL_PATH.assets, REL_PATH.meshes)
        self.materials = os.path.join(self.root, REL_PATH.assets, REL_PATH.materials)
        self.textures = os.path.join(self.root, REL_PATH.assets, REL_PATH.textures)


@dataclasses.dataclass
class Extensions:
    """
    This class contains the extensions for the files used in the project.
    It is used to manage the extensions of the files used in the project.\n

    It contains the following attributes:
    - shader_vert: This attribute contains the extension of the vertex shader files.
    - shader_frag: This attribute contains the extension of the fragment shader files.
    - mesh: This attribute contains the extension of the mesh files.
    - material: This attribute contains the extension of the material files.
    - texture: This attribute contains the extension of the texture files.
    """
    shader_vert: str = ".vert.glsl"
    shader_frag: str = ".frag.glsl"
    mesh: str = ".obj"
    material: str = ".mtl"
    texture: str = ".png"


class KeyBinds:
    """
    This class contains the key bindings for the project.
    It is used to manage the key bindings of the project.\n

    It contains the following attributes:
    - move_forward: This attribute contains the key for moving forward.
    - move_backward: This attribute contains the key for moving backward.
    - move_left: This attribute contains the key for moving left.
    - move_right: This attribute contains the key for moving right.
    - jump: This attribute contains the key for jumping.
    - sneak: This attribute contains the key for sneaking.
    - escape: This attribute contains the key for escaping.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Build the key bindings for the project.
        """
        self.move_forward: int = KEY_DICT.get("W", 256)
        self.move_backward: int = KEY_DICT.get("S", 256)
        self.move_left: int = KEY_DICT.get("A", 256)
        self.move_right: int = KEY_DICT.get("D", 256)
        self.jump: int = KEY_DICT.get("SPACE", 256)
        self.sneak: int = KEY_DICT.get("LSHIFT", 256)
        self.escape: int = KEY_DICT.get("ESCAPE", 256)


REL_PATH: RelPath = RelPath()
ABS_PATH: AbsPath = AbsPath()
EXTENSIONS: Extensions = Extensions()

WINDOW_NAME: str = "OpenGL"
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
NEAR: float = 0.1
FAR: float = 50.0

BORDER: float = 250.0
PLAYER_SIZE: float = 1.8

CURSOR_SPEED: float = 0.1
ZOOM_SPEED: float = 3.0
MIN_ZOOM: float = 10.0
MAX_ZOOM: float = 90.0
MOVE_SPEED: float = 5.0
JUMP_HEIGHT: float = 3.0
SNEAK_HEIGHT: float = 3.0

KEY_DICT: dict[str, int] = {
    "A": glfw.KEY_A,
    "B": glfw.KEY_B,
    "C": glfw.KEY_C,
    "D": glfw.KEY_D,
    "E": glfw.KEY_E,
    "F": glfw.KEY_F,
    "G": glfw.KEY_G,
    "H": glfw.KEY_H,
    "I": glfw.KEY_I,
    "J": glfw.KEY_J,
    "K": glfw.KEY_K,
    "L": glfw.KEY_L,
    "M": glfw.KEY_M,
    "N": glfw.KEY_N,
    "O": glfw.KEY_O,
    "P": glfw.KEY_P,
    "Q": glfw.KEY_Q,
    "R": glfw.KEY_R,
    "S": glfw.KEY_S,
    "T": glfw.KEY_T,
    "U": glfw.KEY_U,
    "V": glfw.KEY_V,
    "W": glfw.KEY_W,
    "X": glfw.KEY_X,
    "Y": glfw.KEY_Y,
    "Z": glfw.KEY_Z,
    "0": glfw.KEY_0,
    "1": glfw.KEY_1,
    "2": glfw.KEY_2,
    "3": glfw.KEY_3,
    "4": glfw.KEY_4,
    "5": glfw.KEY_5,
    "6": glfw.KEY_6,
    "7": glfw.KEY_7,
    "8": glfw.KEY_8,
    "9": glfw.KEY_9,
    "SPACE": glfw.KEY_SPACE,
    "ESCAPE": glfw.KEY_ESCAPE,
    "ENTER": glfw.KEY_ENTER,
    "TAB": glfw.KEY_TAB,
    "LSHIFT": glfw.KEY_LEFT_SHIFT,
    "LCTRL": glfw.KEY_LEFT_CONTROL
}
KEY_BINDS: KeyBinds = KeyBinds()
