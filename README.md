<p align="center">
    <img src="resources/title.png" alt="title" />
</p>

---

Goodoo is an experimental 2D platformer video game which started as a broken student project and is built with
[Pygame](https://github.com/pygame/pygame).  
Its name has been chosen randomly and has no specific meaning.
This game is the result of many redesigns through the years by an inexperienced developer who has no idea how game
design works.  
And yes, I commit on master, I should burn in hell for that.

## Requirements

```
pip install -r requirements.txt
```

## Use

```
python3 goodoo.py
```

You can run with AZERTY keys with:

```
python3 goodoo.py AZERTY
```

## Gameplay

Your goal is to reach the top of the cave you're trapped in. You've got to do this quickly as lava will start to rise
once a certain height is reached.

You can click to project yourself on the walls like a true Spider-Man and move yourself around while you're doing it by
using the following keys.

| Action       | Key (QWERTY)  |
|--------------|:-------------:|
| fire grapple | `left click`  |
| left         |  `a` / `up`   |
| down         | `s` / `down`  |
| right        | `d` / `right` |

## I don't like OOP :(

Object-Oriented is cool for APIs and polymorphism and all, but when having a linear execution it's just
overkill and added complexity for nothing, with attributes modified anywhere just like they're global
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