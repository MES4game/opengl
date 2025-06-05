# Skeleton code for PyOpenGL

This is the skeleton code for creating graphics applications using OpenGL and Python.


## Installation

You would need some libraries in your machine. To install them, simply run:
```bash
pip install -r requirements.txt
```


## Run the Application

To launch the window, simply run (while in the same directory as this file):
```bash
python3 main.py
```


# Project: Rubik's Cube Simulator
This project is a Rubik's Cube simulator using OpenGL and Python. It allows you to visualize and interact with a 3D model of a Rubik's Cube, providing basic controls to manipulate the cube.


## Configuration
You can change the configuration of the application by editing the `src/utils.py` file.


## In-game Controls
- ESCAPE = close game

- ZQSD = move camera
  - Z = forward
  - Q = left
  - S = backward
  - D = right
- MOUSE WHEEL = zoom in/out camera
- MOUSE = rotate camera

- L = lamp of desk

- arrows = rotate rubiks cube
- 0-9 = action : (WIP)
  - 1 = top: turn left (WIP)
  - 2 = top: turn right (WIP)
  - 3 = left: turn top (WIP)
  - 4 = left: turn bottom (WIP)
  - 5 = right: turn top (WIP)
  - 6 = right: turn bottom (WIP)
  - 7 = bottom: turn left (WIP)
  - 8 = bottom: turn right (WIP)
  - 9 = front face: turn left (WIP)
  - 0 = front face: turn right (WIP)
Actions to use the cube are still buggy, so we don't recomend to use them.
