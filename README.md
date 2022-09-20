<p align="center">
    <img src="resources/title.png" alt="title" />
</p>

---

Goodoo is an experimental 2D platformer video game built with [Pygame](https://github.com/pygame/pygame).  
Its name has been chosen randomly and has no specific meaning.
This game is the result of many redesigns through the years by an inexperienced developer who has no idea how game
design works.
And yes, I commit on master, I should burn in hell for that.

## Requirements

```
pip install -r requirements.txt
```

- [pygame](https://pypi.org/project/pygame/)
- [numpy](https://pypi.org/project/numpy/)
- [scipy](https://pypi.org/project/scipy/)

## Use

```
python goodoo.py
```

## Gameplay

*WIP*

Your goal is to reach the top of the cave you're trapped in.  
Because the moving mechanism constantly changes as I work on this, just try to click everywhere, and you should get some
results.

## Data-Oriented Programming

This project tries to implement **some** principles of the paradigm of *Data-Oriented Programming*
[as described by Yehonathan Sharvit](https://blog.klipse.tech/dop/2022/06/22/principles-of-dop.html).  
This is done as an experiment for myself and to show to my fellow co-workers that you can actually do something with
this thing.

This program respects :

- **Data and code separation** - to free the program from any object dependency graph or spaghetti code, and making it a
  bit more linear to read than classic OOP. This is done by having separate modules for data and functions.
- **Immutable data** - to minimize side effects and forcing the use of pure functions. This is achieved by using
  python's frozen
  [dataclasses](https://docs.python.org/3/library/dataclasses.html).

---

<img src="resources/goodoo.gif" alt="gif">&nbsp;*That's all folks!*</img>