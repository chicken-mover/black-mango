# Black Mango

Please make sure to add docstrings to everything and adhere to the
[style guide](https://github.com/chicken-mover/black-mango/wiki/Style-guide).

Git commit messages should follow 
[the standard format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Requirements

* Make sure you have Pyglet installed
* In all commands, `python` refers to a Python 2.7 interpreter.
* For building binary executables, you will need
  [PyInstaller](http://www.pyinstaller.org/):
```bash
$ git clone git://github.com/pyinstaller/pyinstaller.git
$ cd pyinstaller
$ sudo python setup.py install
```

## Setup instructions for development

Simply clone the repository and run `setup.py develop`, like so:

```bash
$ git clone git@github.com:chicken-mover/black-mango.git
$ cd black-mango
$ sudo python setup.py develop
```

## Build instructions

After running the `setup.py develop` command above, you can run the `build.sh`
script from the project directory like so:
```bash
$ ./build.sh make-debug
```

The full set of options is as follows:
* `make` - Build the executable using PyInstaller.
* `make-debug` - Run `make`, but with all debugging options enabled.
* `clean` - Clean up all build output files.

If `build.sh` isn't executable, fix the permissions with:
```bash
$ chmod u+x build.sh
```

Any extra options beyond the first will be passed directly to PyInstaller. See
[the manual](http://www.pyinstaller.org/export/d3398dd79b68901ae1edd761f3fe0f4ff19cfb1a/project/doc/Manual.html)
for more information, or do `pyinstaller --help` at the command line.

## Progress and notes

Please see the [wiki](https://github.com/chicken-mover/black-mango/wiki).
