# Pyweek 39 Game Jam Entry!

![alt text](https://raw.githubusercontent.com/d-orm/pyweek_39_game/refs/heads/main/screenshot.png "Screenshot")

## DATASTREAM DEFENDER

* Defend the datastream from the incoming obstacles!
* Use ARROW KEYS to move and press/hold SPACE to shoot
* You can shoot down the obstacles to gain money
* Use the money to buy health and upgrades (press F)
* Shooting also costs a small amount of money
* You'll lose health if you collide with an enemy
* You'll also lose health when enemies reach the top

**Hint: Don't forget to get upgrades and health!**

### [Play on the web here!](https://djorm.pyscriptapps.com/datastream-defender) 

Mobile controls are not implemented due to lack of time, so desktop only.

-----------------


This game uses [zengl](https://github.com/szabolcsdombi/zengl/) to render with OpenGL/WebGL, [webwindow](https://github.com/szabolcsdombi/webwindow) for [Pyscript](https://pyscript.com/) window and input handling, [pygame-ce](https://github.com/pygame-community/pygame-ce) for utility functions like collisions and image loading (+ audio and window when running natively), and [numpy](https://github.com/numpy/numpy) for data manipulation.

Image assets were generated with [DALL*E 3](https://openai.com/index/dall-e-3/), music generated with [SUNO](https://suno.com/), sfx created with [JSFXR](https://sfxr.me/), font from https://fonts.google.com/. The shader code for the background was adapted from/inspired [this](https://www.shadertoy.com/view/3lBBWG) shadertoy contribution

-----------------

You can also checkout the [repo](https://github.com/d-orm/pyweek_39_game) to run locally.

To run in local browser:
```bash
python -m python -m http.server -d .
```
Then navigate to http://localhost:8000/ 
(internet connection required still for dependencies)

Or run natively:
```bash
pip install zengl pygame-ce numpy
python -m main
```

