# - Work still in progress -

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

- [pygame](https://pypi.org/project/pygame/) ```pip install pygame```
- [numpy](https://pypi.org/project/numpy/) ```pip install numpy```
- [scipy](https://pypi.org/project/scipy/) ```pip install scipy```

## Use

```
python goodoo.py
```

## Gameplay [TODO]

## Data-Oriented Programming

This project tries to implement some (but not all) principles of the paradigm of *Data-Oriented Programming*
[as described by Yehonathan Sharvit](https://blog.klipse.tech/).
This is done as an experiment for myself and to show to my fellow co-workers that you can actually do something with 
this thing.

The program **respects** :

- **Data and code separation** - to free the program from any object dependency graph or spaghetti code, and making it a
bit more linear to read than classic OOP. This is done by having separate modules for data and functions.

- **Immutable data** - to minimize side effects. This is achieved by using python's frozen 
[dataclasses](https://docs.python.org/3/library/dataclasses.html).


The program **doesn't respect**  :

- **Generic Data structure** - as I want to ensure model consistency by having each data of same type having the same 
shape.


The program **doesn't use** :

- **Data comparability by value**

- **Literal representation of the data**

---

<img src="resources/animation.gif" alt="gif"/>