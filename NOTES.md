

* http://stackoverflow.com/questions/8556589/scale-resolution-in-pyglet
* https://ep2013.europython.eu/conference/talks/distributing-python-programs-through-pyinstaller
* http://tartley.com/?p=353

Temporary sprites:
* http://www.spriters-resource.com/playstation/fft/

Building with Cython:
* https://github.com/cython/cython/wiki/PackageHierarchy

## Menu sections

### Load/New

* Display title cards on new/loaded games
* Get levels flowing into each other
* Set OOB rules for room edges? Are all roms the same size?

### Save games

* (Scrolling of long game lists gonna be a drag)

### Options & controls

* Fullscreen/windowed
* Set resolution (will require writing grid to autoadjust to window size)
* Edit controls
    - Primary move keys: [W,A,S,D]
    - Primary action key: [ENTER]
    - Secondary move keys [UP,DOWN,LEFT,RIGHT]
    - Secondary action key: [SPACE]

# Crazy shit
* *Could* compile assets into relevant python objects, pickle them, and then 
  load them via import statements. (pyglet.image.load returns a pickleable 
  object; fonts and other files could be read into StringIO buffers and 
  pickled). This should possibly be re-examined again later when prepping for 
  distribution


# Compile everything using Cython
(also good for doing correctness checks on the code)
```bash
$ find . -type f -name '*.py' -exec $PY27/cython -f {} \;
```

## Cleanup from that compile:
```bash
$ sudo find . -type f -name '*.c' -exec rm -v {} \;
$ sudo find . -type f -name '*.py[co]' -exec rm -v {} \;
```