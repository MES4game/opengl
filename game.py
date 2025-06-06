"""
game module
===========

Module to/that # TODO: set docstring

Functions
---------
    # TODO: set functions
"""


# built-in imports
import math
import typing
from enum import IntEnum
# pip imports
import pyglm.glm as glm
import glfw  # type: ignore
# local imports
import src


class State(IntEnum):
    DEFAULT = 0
    ROTATING = 1
    TURNING = 2


class AnimationType(IntEnum):
    ROT_R = 0
    ROT_L = 1
    ROT_U = 2
    ROT_D = 3
    TURN_FL = 4
    TURN_FR = 5
    TURN_UL = 6
    TURN_UR = 7
    TURN_LU = 8
    TURN_LD = 9
    TURN_RU = 10
    TURN_RD = 11
    TURN_DL = 12
    TURN_DR = 13
    NONE = 14


def roundQuatToPi(rot: glm.quat) -> glm.quat:
    matrix: glm.mat4x4 = glm.mat4_cast(rot)
    snapped: glm.mat3x3 = glm.mat3(matrix)
    for i in range(3):
        for j in range(3):
            snapped[i][j] = 0.0 if abs(snapped[i][j]) < 0.5 else (1.0 if snapped[i][j] > 0 else -1.0)
    return glm.quat_cast(snapped)


class Game:
    """
    Game class
    ==========

    Class to/that # TODO: set docstring

    Attributes:
        # TODO: set attributes
    Methods
    -------
        # TODO: set methods
    """
    def __init__(
            self: typing.Self,
            renderer: src.Renderer,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            renderer (`src.Renderer`): The renderer.
        Raises:
            # TODO: set exceptions
        """
        self.state: State = State.DEFAULT
        self.animation_type: AnimationType = AnimationType.NONE
        self.animation_time: float = 0.0
        self.builded: bool = False

        self.jumping: bool = False
        self.jump_time: float = 0.0

        self.table: src.shapes.Node = src.shapes.Node()
        self.lamp: src.shapes.Light = src.shapes.Light(
            shader_name="basic",
            mesh_name="cylinder",
            color=glm.vec3(0),
            light_color=glm.vec3(1, 1, 0)
        )

        self.cubies: list[src.shapes.Node] = [
            src.shapes.Node(shader_name="basic_texlight", mesh_name="cubie", texture_name="colors", has_light=True)
            for _ in range(27)
        ]
        self.root = self.cubies[13]
        self.sub_root = src.shapes.Node(self.root)

        renderer.scene.addElements(
            root=self.root,
            table=self.table
        )

        self.postInit()

    def postInit(
            self: typing.Self,
            /
            ) -> None:
        """
        Method to/that # TODO: set docstring

        Args:
            # TODO: set args
        Raises:
            # TODO: set exceptions
        """
        plank = src.shapes.basics.Node(shader_name="basic_tex", mesh_name="cube", texture_name="wood")
        plank.addElements(
            lamp=self.lamp,
            leg1=src.shapes.basics.Cylinder(texture_name="wood"),
            leg2=src.shapes.basics.Cylinder(texture_name="wood"),
            leg3=src.shapes.basics.Cylinder(texture_name="wood"),
            leg4=src.shapes.basics.Cylinder(texture_name="wood"),
            arrow=src.shapes.basics.Triangle(color=glm.vec3(1, 0, 0))
        )
        plank.setCoord(pos=glm.vec3(0, 1.05, 0), size=glm.vec3(1, 0.1, 1))
        self.lamp.setCoord(
            pos=glm.vec3(-0.4, 0.8, 0.4),
            size=glm.vec3(0.1, 3, 0.1)
        )
        plank.children["leg1"].setCoord(pos=glm.vec3(0.4, -5.05, 0.4), size=glm.vec3(0.1, 10, 0.1))
        plank.children["leg2"].setCoord(pos=glm.vec3(0.4, -5.05, -0.4), size=glm.vec3(0.1, 10, 0.1))
        plank.children["leg3"].setCoord(pos=glm.vec3(-0.4, -5.05, -0.4), size=glm.vec3(0.1, 10, 0.1))
        plank.children["leg4"].setCoord(pos=glm.vec3(-0.4, -5.05, 0.4), size=glm.vec3(0.1, 10, 0.1))
        plank.children["arrow"].setCoord(pos=glm.vec3(0, 0.51, 0.4), rot=glm.angleAxis(math.pi / 2, src.utils.YAW_AXIS), size=glm.vec3(0.1, 1, 0.1))
        self.table.addElements(plank=plank)
        self.table.setCoord(pos=glm.vec3(0, 0, -0.25))

        self.cubies[14].addElements(logo=src.shapes.basics.Square(texture_name="logo_cia_2048", has_light=True))
        self.cubies[14].children["logo"].setCoord(
            pos=glm.vec3(0, 0, 0.5001),
            rot=(glm.angleAxis(math.pi / 2, src.utils.ROLL_AXIS) * glm.angleAxis(math.pi / 2, src.utils.PITCH_AXIS)),
            size=glm.vec3(0.9)
        )

        pos = (-1, 0, 1)
        for x in pos:
            for y in pos:
                for z in pos:
                    idx = (x + 1) * 9 + (y + 1) * 3 + (z + 1)
                    self.cubies[idx].setCoord(pos=glm.vec3(x, y, z))

        self.root.addElements(*[cubie for cubie in self.cubies if cubie != self.root])
        self.root.setCoord(pos=glm.vec3(0, src.utils.PLAYER_SIZE * 0.65, 0), size=glm.vec3(1/30))

    def checkAnimation(
            self: typing.Self,
            delta_time: float,
            /
            ) -> None:
        """
        Function to/that # TODO: set docstring

        Args:
            delta_time (`float`): the time elapsed since last frame in seconds.
        Raises:
            # TODO: set exceptions
        """
        self.animation_time += delta_time

        if self.animation_time >= 1:
            self.unbuild()

            for cubie in self.cubies:
                if cubie != self.root:
                    cubie.pos = glm.round(cubie.pos)
                cubie.rot = roundQuatToPi(cubie.rot)
                cubie.to_render = cubie.to_update = True

            self.state = State.DEFAULT
            self.animation_type = AnimationType.NONE
            self.animation_time = 0.0

    def rotate(
            self: typing.Self,
            delta_time: float,
            /
            ) -> None:
        """
        Function to/that # TODO: set docstring

        Args:
            delta_time (`float`): the time elapsed since last frame in seconds.
        Raises:
            # TODO: set exceptions
        """
        if self.state != State.ROTATING:
            return

        match self.animation_type:
            case AnimationType.ROT_U:
                axis = src.utils.PITCH_AXIS
                sign = -1
            case AnimationType.ROT_L:
                axis = src.utils.YAW_AXIS
                sign = -1
            case AnimationType.ROT_R:
                axis = src.utils.YAW_AXIS
                sign = 1
            case AnimationType.ROT_D:
                axis = src.utils.PITCH_AXIS
                sign = 1
            case _: return

        self.root.rotate(glm.angleAxis(sign * math.pi / 2 * delta_time, axis))

        self.checkAnimation(delta_time)

    def turn(
            self: typing.Self,
            delta_time: float,
            renderer: src.Renderer,
            /
            ) -> None:
        """
        Function to/that # TODO: set docstring

        Args:
            delta_time (`float`): the time elapsed since last frame in seconds.
        Raises:
            # TODO: set exceptions
        """
        if self.state != State.TURNING:
            return

        if not self.builded:
            self.build()
            self.animation_time = 0.0

        match self.animation_type:
            case AnimationType.TURN_FL | AnimationType.TURN_FR: axis = src.utils.ROLL_AXIS
            case AnimationType.TURN_UL | AnimationType.TURN_UR: axis = src.utils.YAW_AXIS
            case AnimationType.TURN_LU | AnimationType.TURN_LD: axis = src.utils.PITCH_AXIS
            case AnimationType.TURN_RU | AnimationType.TURN_RD: axis = src.utils.PITCH_AXIS
            case AnimationType.TURN_DL | AnimationType.TURN_DR: axis = src.utils.YAW_AXIS
            case _: return

        match self.animation_type:
            case AnimationType.TURN_FL: sign = -1
            case AnimationType.TURN_UL: sign = -1
            case AnimationType.TURN_LU: sign = -1
            case AnimationType.TURN_RU: sign = -1
            case AnimationType.TURN_DR: sign = -1
            case _: sign = 1

        self.sub_root.rotate(glm.angleAxis(sign * math.pi / 2 * delta_time, axis))
        self.sub_root.updateModelMatrix(True)
        self.sub_root.render(renderer, True)

        self.checkAnimation(delta_time)

    def build(
            self: typing.Self,
            /
            ) -> None:
        """
        Function to/that # TODO: set docstring

        Args:
            # TODO: set args
        Raises:
            # TODO: set exceptions
        """
        eps = glm.max(self.root.size)

        match self.animation_type:
            case AnimationType.TURN_FL | AnimationType.TURN_FR: f = lambda x: x.pos.z > eps and x != self.root
            case AnimationType.TURN_UL | AnimationType.TURN_UR: f = lambda x: x.pos.y > eps and x != self.root
            case AnimationType.TURN_LU | AnimationType.TURN_LD: f = lambda x: x.pos.x < -eps and x != self.root
            case AnimationType.TURN_RU | AnimationType.TURN_RD: f = lambda x: x.pos.x > eps and x != self.root
            case AnimationType.TURN_DL | AnimationType.TURN_DR: f = lambda x: x.pos.y < -eps and x != self.root
            case _:
                return

        self.sub_root = src.shapes.Node(self.root)
        self.sub_root.setCoord(pos=self.root.pos, size=self.root.size)
        self.sub_root.addElements(*filter(f, self.cubies))

        self.builded = True

    def unbuild(
            self: typing.Self,
            /
            ) -> None:
        """
        Function to/that # TODO: set docstring

        Args:
            # TODO: set args
        Raises:
            # TODO: set exceptions
        """
        if not self.sub_root.children:
            return

        for cubie in self.sub_root.children.values():
            cubie.rot = self.sub_root.rot * cubie.rot
            cubie.pos = self.sub_root.rot * cubie.pos

        self.root.addElements(*self.sub_root.children.values())
        self.root.subElements(self.sub_root)

        self.sub_root.children.clear()
        self.sub_root.cleanRessources()

        self.builded = False


GAME: Game


def initGame(
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
    global GAME

    GAME = Game(renderer)


def loopGame(
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
    global GAME

    if glfw.get_key(renderer.window, src.utils.KEY_BINDS.lamp) == glfw.PRESS:
        if GAME.lamp in renderer.lights:
            renderer.lights.remove(GAME.lamp)
            GAME.lamp.setColor(glm.vec3(0))
        else:
            renderer.lights.append(GAME.lamp)
            GAME.lamp.setColor(GAME.lamp.light_color)

    if not GAME.jumping and glfw.get_key(renderer.window, src.utils.KEY_BINDS.jump) == glfw.PRESS:
        GAME.jumping = True
        GAME.jump_time = 0.0

    if GAME.jumping and GAME.jump_time < src.utils.JUMP_TIME:
        renderer.camera.pos.y += src.utils.JUMP_HEIGHT * delta_time
        GAME.jump_time += delta_time
    elif abs(renderer.camera.pos.y - src.utils.PLAYER_SIZE) < 1e-6:
        GAME.jumping = False

    renderer.camera.pos.y = max(src.utils.PLAYER_SIZE, renderer.camera.pos.y - 9.81 * delta_time)

    match GAME.state:
        case State.DEFAULT:
            for k, t in (
                        (src.utils.KEY_BINDS.rotate_up, AnimationType.ROT_U),
                        (src.utils.KEY_BINDS.rotate_left, AnimationType.ROT_L),
                        (src.utils.KEY_BINDS.rotate_right, AnimationType.ROT_R),
                        (src.utils.KEY_BINDS.rotate_down, AnimationType.ROT_D),
                        (src.utils.KEY_BINDS.turn_front_left, AnimationType.TURN_FL),
                        (src.utils.KEY_BINDS.turn_front_right, AnimationType.TURN_FR),
                        (src.utils.KEY_BINDS.turn_up_left, AnimationType.TURN_UL),
                        (src.utils.KEY_BINDS.turn_up_right, AnimationType.TURN_UR),
                        (src.utils.KEY_BINDS.turn_left_up, AnimationType.TURN_LU),
                        (src.utils.KEY_BINDS.turn_left_down, AnimationType.TURN_LD),
                        (src.utils.KEY_BINDS.turn_right_up, AnimationType.TURN_RU),
                        (src.utils.KEY_BINDS.turn_right_down, AnimationType.TURN_RD),
                        (src.utils.KEY_BINDS.turn_down_left, AnimationType.TURN_DL),
                        (src.utils.KEY_BINDS.turn_down_right, AnimationType.TURN_DR),
                    ):
                if glfw.get_key(renderer.window, k) == glfw.PRESS:
                    GAME.animation_type = t
                    break

            if GAME.animation_type != AnimationType.NONE:
                GAME.animation_time = 0.0
                if GAME.animation_type in (AnimationType.ROT_L, AnimationType.ROT_R, AnimationType.ROT_U, AnimationType.ROT_D):
                    GAME.state = State.ROTATING
                    GAME.rotate(delta_time)
                else:
                    GAME.state = State.TURNING
                    GAME.turn(delta_time, renderer)

        case State.ROTATING: GAME.rotate(delta_time)
        case State.TURNING:  GAME.turn(delta_time, renderer)
