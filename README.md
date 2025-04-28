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


## TODO

- [ ] `game/*` and `main.py`: implement a function for key callback and pass it to the renderer
- [ ] `src/renderer.py`: implement a state for the scene and the camera to control when they update (like when in pause, a menu, etc.)
- [ ] `src/renderer.py`: implement a render for menus (like the main menu, pause menu, etc.)
- [ ] `main.py`: change keyboard handle to use GLFW callback instead of the main loop
- [ ] `src/renderer.py`: implement every GLFW necessary callback (like window unfocus, mouse button, etc.)
- [ ] `game/*` and `main.py`: implement functions for keyboard, mouse and scroll callback and pass them to the renderer
- [ ] `src/renderer.py` and `src/shapes/shape.py`: implement a sun (instead of using the player as light source)
- [ ] `assets/shaders/*light.glsl`: implement the possibility to use multiple lights
- [ ] `assets/shaders/*light.glsl`: improve the model (e.g. add the distance to the light, etc.)
- [ ] `src/light.py`: implement a light class
- [ ] `src/scene.py`: implement a lights list and pass them to shapes for render
- [ ] `src/shapes/{shape,node}.py`: implement use of multiple lights
- [ ] `src/shapes/animation.py`: implement a class to store animation
- [ ] `src/shapes/{shape,node}.py`: implement a state that will be used to animate shapes and make impossible to change them during the animation
- [ ] `src/main.py`: implement animations and do them
- [ ] `src/*` and `main.py`: complete every docstrings
- [ ] `src/*` and `main.py`: add comment inside functions/methods
- [ ] `src/camera.py`: implement every camera type
- [ ] `src/*` and `main.py`: find and complete every `# TODO`
- [ ] `README.md`: rework the README
