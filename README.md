# Pygame platformer game

## Description

This is a platformer game made with Python 3 and Pygame library. It follows closely DaFluffyPotato's Youtube video tutorial: 
[![Pygame Platformer Tutorial - Full Course]([https://img.youtube.com/vi/2gABYM5M0ww/0.jpg)](https://www.youtube.com/watch?v=2gABYM5M0ww)

All asset and code credits goes to him.

## Running the game.py

You need to have Python 3 installed and added to the PATH variables.
You also need Pygame library for Python, I suggest installing the community version pygame-ce but base version should work aswell.

```
pip install pygame-ce
```
or
```
py pip install pygame-ce
```
You also need the 'data' folder for the game assets which you can get from DaFluffyPotato's website: https://dafluffypotato.com/assets/pg_tutorial

In the 00_resources.zip file should be a folder names data which you need to place to the projects root.

If everything is OK you should be able to run the main file game.py with the following command:

```
py game.py
```

## Playing the game

Moving and jumping is controlled with the arrow keys and dash attack is bound to 'x' key.

The object is to get rid of all the enemies on the level. 
The game has three levels with increasing difficulty. 
You can exit the game by closing the window.

## Using the map editor

Project includes a rudimentary map editor. Which you can run with command:

```
py editor.py
```

The editor reads from and writes to the file 'map.json' in project root. 
You can edit the playable maps by copying the map's json from data/maps/ folder in to the map.json and otherway around. 
Adding new maps to the game is done by continuing the numbering in data/maps/ folder.

Controls for the editor:

'Mouse scroll' changes the placable tile.

'Shift + mouse scroll' changes the placable tile variation.

'Left mouse button' places the tile.

'Right mouse button' deletes the tile cursor is hovering on.

'o' saves the current map to map.json

'g' toggles the grid on and off.

Note! 

As a rule of thumb place platform tiles into grid and player and enemy spawns to off grid.
You can place the decor tiles either on to grid or off it.

The map will cause the game to crash if player or enemy spawners are placed on grid.

## Building the game

The game can be build using PyInstaller:

```
py -m pip install PyInstaller
```

And the building is done with command:

```
py -m PyInstaller game.py --noconsole
```

The 'data' folder needs to be added to the newly created 'dist/game/' folder on the same level as the game.exe file.
