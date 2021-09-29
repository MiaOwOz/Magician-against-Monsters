# Magician agains Monsters

This is a simple text-based Python game, aimed to be ran on a Micro-Controller running CircuitPython. It can also be run on a normal computer using Python, altough you'll need to remove the CircuitPython specific lines of code.
There will be a Python-file for "normal" computers once the game is finished!

## Installation / Getting Started

Just clone the repository. Inside the ZIP-file, you'll find a game.py, which is the game's code.
If you want to use the game on your computer, comment out the lines 3, 4, 11-16, 142-146 and 149-153. It will then run.

If you're running CircuitPython, you just need to put the .py-file onto the CIRCUITPYTHON-Drive and run it using the following line in the code.py on your Micro Controller:
```
import game.py
```
If you've done that, it will automatically run. Connect to the REPL using your IDE (like MU Editor). You will automatically be prompted to input your name.
