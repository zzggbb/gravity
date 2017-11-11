![gravity.png](gravity.png)

This is a 2 dimensional simulator of the forces of gravity.

### Getting Started

```
$ git clone https://github.com/zzggbb/gravity
$ cd gravity
$ python3 -m virtualenv .
$ pip install -r requirements.txt
$ python3 gravity.py
```

### Features
* play/pause the simulation
* seek forwards/backwards in time
* add/remove objects
* change the properties of an object
  * color
  * mass
  * density
  * radius
  * position
  * velocity
  * acceleration

* change the type of collision undergone by objects
  * perfectly elastic (objects bounce)
  * perfectly inelastic (objects stick)
  * no collision

* toggle the display of velocity and acceleration
vectors
