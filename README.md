# Black Mango

Please make sure to add docstrings to everything and adhere to the
[style guide](https://github.com/chicken-mover/black-mango/wiki/Style-guide).

Git commit messages should follow 
[the standard format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Requirements

* `pyglet` for GUI/OpenGL support
* `mock` and `nose` for testing
* `setuptools` to install all other dependencies automatically.
* In all commands, `python` refers to a Python 2.7 interpreter.

### Build requirements

* For building binary executables, you will need
  [PyInstaller](http://www.pyinstaller.org/):

```bash
$ git clone git://github.com/pyinstaller/pyinstaller.git
$ cd pyinstaller
$ sudo python setup.py install
```

* You will also need access to a Bash interpreter. On Windows, Cygwin should
  suffice.

## Setup instructions for development

Simply clone the repository and run `setup.py develop`, like so:

```bash
$ git clone git@github.com:chicken-mover/black-mango.git
$ cd black-mango
$ sudo python setup.py develop
```

This should also install dependencies, assuming you have `setuptools` and `pip`
installed correctly.

If you want to activate the git hooks that come with the repository, you should
also do the following, in the base directory of the project:

```bash
$ mv .git/hooks .git/hooks-backup
$ ln -s ../hooks .git/hooks
$ chmod u+x hooks/*
```

This will help with things like automatic validation of version numbers during
commit.

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
[the manual](http://www.pyinstaller.org/export/develop/project/doc/Manual.html)
for more information, or do `pyinstaller --help` at the command line.

## Running tests

Run `sudo python setup.py test` in the project root to run all unit tests.

## Progress and notes

Please see the [wiki](https://github.com/chicken-mover/black-mango/wiki).
