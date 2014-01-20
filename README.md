# Black Mango

Please make sure to add docstrings to everything and adhere to the
[style guide](https://github.com/chicken-mover/black-mango/wiki/Style-guide).

Git commit messages should follow 
[the standard format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Requirements

* `pyglet` for GUI/OpenGL support
* `mock` and `nose` for testing
* `setuptools` to install all other dependencies automatically.
* In all commands, `python` refers to a Python 2.7 interpreter. If you do not
  have Python 2.7 installed, you can download a prepackaged installer from the
  [Python website](http://www.python.org/getit/) (on Windows or OS X) or, under
  Linux, install it on your favorite package manager (Arch:
  `sudo pacman -S python2`; Debian: `sudo apt-get install python`)

### Build requirements

**NB.:** You do not need to build binaries to test the functionality of the
game. Binaries should only be build when you need to actually test whether the
game builds correctly on a given system. Skip to "Setup instructions for
development" for infomation on normal testing.

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

Start by cloning the repository and installing the Git hooks, which will do some
basic checks when you commit/pull in the future.

Simply clone the repository and run `setup.py develop`, like so:

```bash
$ git clone git@github.com:chicken-mover/black-mango.git
$ cd black-mango
$ bash scripts/install-hooks.sh
```

You should then install Black Mango as a development module. The `run-setup.sh`
script will take care of selecting the proper Python binary to use, assuming you
have Python 2.7 installed. If you do not, you cannot run Black Mango.

```bash
$ bash run-setup.sh
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
[the manual](http://www.pyinstaller.org/export/develop/project/doc/Manual.html)
for more information, or do `pyinstaller --help` at the command line.

## Progress and notes

Please see the [wiki](https://github.com/chicken-mover/black-mango/wiki).
