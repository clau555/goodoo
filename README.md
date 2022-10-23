<p align="center">
    <img src="resources/title.png" alt="title" />
</p>

---

Goodoo is a procedural 2D platformer video game which started as a broken student project and is built with
[Pygame](https://github.com/pygame/pygame).  
Its name has been chosen randomly and has no specific meaning.
This game is the result of many redesigns through the years by an inexperienced developer who has no idea how game
design works.  
And yes, I commit on master, I should burn in hell for that (and don't look at the commit history it's an absolute mess)
.

## Running from sources

This program requires python installed.

First download the repository or clone it to your computer.

```bash
git clone https://github.com/clau555/goodoo.git
```

You can use pip to install the required libraries.

```bash
pip install -r requirements.txt
```

Then run the main file.

```bash
python3 goodoo.py
```

You can run with AZERTY keys with:

```bash
python3 goodoo.py AZERTY
```

## Gameplay

You're an animated small ball of goo that fell into a cave full of lava at the bottom and your goal is to reach the top
of the cave to escape.  
You've got to do this quickly as lava will start to rise once a certain height is reached.  
Be careful on your way as mushrooms will bump you in the opposite way and pointy minerals will kill you instantly.

You can click to project yourself on the walls like a true Spider-Man and move yourself from left to right while you're
in the air.

### Default keys

| Action       |      Key      |
|--------------|:-------------:|
| fire grapple | `left click`  |
| left         | `a` / `left`  |
| right        | `d` / `right` |
| pause        |      `p`      |
| end game     |   `escape`    |

## Cave generation

The goal is to generate a tile cave only opened at the top, where the player can climb to.

The map generation works as grid where we play a cave generator cellular automaton, which creates several rooms inside
the map.  
We then dig connections between neighboring rooms to make sure any rooms can be accessible starting from any other
room.  
A hardcoded hole is dig at the top of the map to create a finish line for the player.

Obstacle tiles are generated randomly on walls, with free space in front of them guaranteeing the player will not be
stuck in its progression.

Non physic tiles, called "decorations" are placed randomly in a separated map, with each decoration type satisfying
its own generation constraint.

## I don't like OOP :(

Object-Oriented is cool for API frameworks and (sometimes) polymorphism, and all, but when having a linear execution
it's just overkill and added complexity for nothing, with attributes modified anywhere just like they're global
variables.  
In that case, instead of going straight for OOP without thinking, consider using functions, and even more functions,
please :cry:

This project tries to implement **some** principles of the Data-Oriented Programming paradigm
[described by Yehonathan Sharvit](https://blog.klipse.tech/dop/2022/06/22/principles-of-dop.html).  
So this program respects :

- **Data and code separation** - to free the program from any object dependency graph or spaghetti code, and making it a
  bit more linear to read than OOP.
- **Immutable data** - to minimize side effects and forcing the use of pure functions. This is achieved by using
  python's frozen [dataclasses](https://docs.python.org/3/library/dataclasses.html).

In the end the code looks like procedural programming with structs and functions, but this is where the idea
came from, and it took me a lot of effort to figure it out in my head, ok ??  
Ok that's enough of me raging over a paradigm and justifying my code.

---

<img src="resources/goodoo.gif" alt="gif">&nbsp;*That's all folks!*</img>