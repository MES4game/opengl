"""
utils module
============
Package: `src`

Module to/that # TODO: set docstring

Classes
-------
- `RelPath`
- `AbsPath`
- `Extensions`
- `KeyBinds`
Globals
-------
- `YAW_AXIS`: Axis to do rotation for yaw angle.
- `PITCH_AXIS`: Axis to do rotation for pitch angle.
- `ROLL_AXIS`: Axis to do rotation for roll angle.
- `ONE_DEG_RAD`: One degree converted to radians.
- `TWO_PI`: `math.pi * 2`.
- `REL_PATH`: Relative paths used for making absolute path.
- `ABS_PATH`: Absolute paths used for finding folders.
- `EXTENSIONS`: Extensions used for files.
- `WINDOW_NAME`: Name displayed for the window.
- `SCREEN_WIDTH`: Width of the window to display.
- `SCREEN_HEIGHT`: Height of the window to display.
- `NEAR`: Distance from wich objects are considered near.
- `FAR`: Distance from wich objects are considered far.
- `BORDER`: Size of the map.
- `BACK_COLOR`: Background color of the scene (sky color).
- `PLAYER_SIZE`: Size of the player in the scene.
- `CAM_SPEED`: Angle speed when moving camera.
- `MIN_CAM_PITCH`: Minimum pitch angle for camera.
- `MAX_CAM_PITCH`: Maximum pitch angle for camera.
- `ZOOM_SPEED`: Angle speed when zooming in/out.
- `MIN_ZOOM`: Minimum angle when zooming in.
- `MAX_ZOOM`: Maximum angle when zooming out.
- `MOVE_SPEED`: Move speed of player.
- `FLY_JUMP_HEIGHT`: Height delta when jumping while flying.
- `FLY_SNEAK_HEIGHT`: Height delta when sneaking while flying.
- `KEY_DICT`: Contains every keys.
- `KEY_BINDS`: Contains every actions with their key binded.
"""


# built-in imports
import os
import typing
import dataclasses
import math
# pip imports
import pyglm.glm as glm
import glfw  # type: ignore
# local imports


@dataclasses.dataclass
class RelPath:
    """
    RelPath class
    =============

    Class to/that # TODO: set docstring

    Attributes:
        src (`str`): relative path (without './' at start) for `src` folder from root of project.
        assets (`str`): relative path (without './' at start) for `assets` folder from root of project.
        shaders (`str`): relative path (without './' at start) for `shaders` folder from `assets` folder.
        meshes (`str`): relative path (without './' at start) for `meshes` folder from `assets` folder.
        textures (`str`): relative path (without './' at start) for `textures` folder from `assets` folder.
    """
    src: str = "src"
    assets: str = "assets"
    shaders: str = "shaders"
    meshes: str = "meshes"
    textures: str = "textures"


@dataclasses.dataclass
class AbsPath:
    """
    AbsPath class
    =============

    Class to/that # TODO: set docstring

    Attributes:
        root (`str`): absolute path for root of project.
        src (`str`): absolute path for `src` folder.
        shaders (`str`): absolute path for `shaders` folder.
        meshes (`str`): absolute path for `meshes` folder.
        textures (`str`): absolute path for `textures` folder.
    Methods
    -------
    - `updatePath`
    """
    root: str = os.path.dirname(os.path.abspath(__file__))
    src: str = ""
    shaders: str = ""
    meshes: str = ""
    textures: str = ""

    def __post_init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring
        """
        self.updatePath()

    def updatePath(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring
        """
        self.src = os.path.join(self.root, REL_PATH.src)
        self.shaders = os.path.join(self.root, REL_PATH.assets, REL_PATH.shaders)
        self.meshes = os.path.join(self.root, REL_PATH.assets, REL_PATH.meshes)
        self.textures = os.path.join(self.root, REL_PATH.assets, REL_PATH.textures)


@dataclasses.dataclass
class Extensions:
    """
    Extensions class
    ================

    Class to/that # TODO: set docstring

    Attributes:
        shader_vert (`str`): extension for vertex shader.
        shader_frag (`str`): extension for fragment shader.
        mesh (`str`): extension for mesh.
        texture (`str`): extension for texture.
    """
    shader_vert: str = ".vert.glsl"
    shader_frag: str = ".frag.glsl"
    mesh: str = ".obj"
    texture: str = ".png"


class KeyDoubleDict:
    """
    KeyDoubleDict class
    ===================

    Class to/that # TODO: set docstring

    Attributes:
        __str_dict (`dict[str, int]`): dict that bind strings to a key number.
        __int_dict (`dict[int, str]`): dict that bind key numbers to a str.
    Methods
    -------
    - `get`
    """
    def __init__(
            self: typing.Self,
            default: dict[str, int],
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            default (`dict[str, int]`): default dict that links strings to keys.
        """
        self.__str_dict: dict[str, int] = {}
        self.__int_dict: dict[int, str] = {}

        for key, value in default.items():
            self.__str_dict[key] = value
            self.__int_dict[value] = key

    @typing.overload
    def get(self: typing.Self, key: int, /) -> str:
        """
        Method to/that # TODO: set docstring

        Args:
            key (`int`): the key number from wich to get a string.
        Returns:
            `str`: the string linked to the key number.
        """
        ...

    @typing.overload
    def get(self: typing.Self, key: str, /) -> int:
        """
        Method to/that # TODO: set docstring

        Args:
            key (`str`): the string from wich to get a key number.
        Returns:
            `int`: the key number linked to the string.
        """
        ...

    def get(
            self: typing.Self,
            key: int | str,
            /
            ) -> str | int:
        if isinstance(key, int):
            return self.__int_dict.get(key, "")
        return self.__str_dict.get(key, -1)


class KeyBinds:
    """
    KeyBinds class
    ==============

    Class to/that # TODO: set docstring

    Attributes:
        move_forward (`int`): Key for move forward action.
        move_backward (`int`): Key for move backward action.
        move_left (`int`): Key for move left action.
        move_right (`int`): Key for move right action.
        jump (`int`): Key for jump action.
        sneak (`int`): Key for sneak action.
        escape (`int`): Key for escape action.
    """
    def __init__(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring
        """
        self.move_forward: int = KEY_DICT.get("W")
        self.move_backward: int = KEY_DICT.get("S")
        self.move_left: int = KEY_DICT.get("A")
        self.move_right: int = KEY_DICT.get("D")
        self.jump: int = KEY_DICT.get("SPACE")
        self.sneak: int = KEY_DICT.get("LSHIFT")
        self.escape: int = KEY_DICT.get("ESCAPE")


YAW_AXIS: glm.vec3 = glm.vec3(0, 1, 0)
PITCH_AXIS: glm.vec3 = glm.vec3(0, 0, 1)
ROLL_AXIS: glm.vec3 = glm.vec3(1, 0, 0)
ONE_DEG_RAD: float = math.pi / 180
TWO_PI: float = math.pi * 2

REL_PATH: RelPath = RelPath()
ABS_PATH: AbsPath = AbsPath()
EXTENSIONS: Extensions = Extensions()

WINDOW_NAME: str = "PyOpenGL"
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
NEAR: float = 0.1
FAR: float = 50.0

BORDER: float = 250.0
BACK_COLOR: tuple[float, ...] = (0.5, 0.7, 1.0, 1.0)
PLAYER_SIZE: float = 1.8

CAM_SPEED: float = ONE_DEG_RAD / 10
MIN_CAM_PITCH: float = -math.pi / 2 + ONE_DEG_RAD
MAX_CAM_PITCH: float = math.pi / 2 - ONE_DEG_RAD
ZOOM_SPEED: float = ONE_DEG_RAD * 3
MIN_ZOOM: float = ONE_DEG_RAD * 10
MAX_ZOOM: float = ONE_DEG_RAD * 90
MOVE_SPEED: float = 5.0
FLY_JUMP_HEIGHT: float = 3.0
FLY_SNEAK_HEIGHT: float = 3.0

KEY_DICT: KeyDoubleDict = KeyDoubleDict({
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
    "LCTRL": glfw.KEY_LEFT_CONTROL,
    # TODO: add more keys
})
KEY_BINDS: KeyBinds = KeyBinds()
