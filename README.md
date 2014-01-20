# Black Mango

Please make sure to add docstrings to everything and adhere to the
[style guide](https://github.com/chicken-mover/black-mango/wiki/Style-guide).

Git commit messages should follow 
[the standard format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Requirements

* `pyglet` and `xmltodict` are `install_requires` entries (ie, you do not need
  to install those dependencies manually).
* ~~`mock` and `nose` for testing~~ (unit tests are on hold)
* `setuptools` must be manually installed before you begin.
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

Start by cloning the repository and `cd`ing into the directory, like so:
```bash
$ git clone git@github.com:chicken-mover/black-mango.git
$ cd black-mango
```

You should then install Black Mango as a development module. The `run-setup.sh`
script will take care of selecting the proper Python binary to use, assuming you
have Python 2.7 installed, as well as installing Black Mango and the Git commit
hooks that will perform automatic validation when pulling and commiting.
```bash
$ bash scripts/run-setup.sh
```

## Build instructions

**Note that the build process is still being worked out, so the instructions
below should be considered highly experimental.**

After running the `setup.py develop` command above, you can run the `build.sh`
script from the project directory like so:
```bash
$ ./scripts/build.sh make-debug
```

The full set of options is as follows:
* `make` - Build the executable using PyInstaller.
* `make-debug` - Run `make`, but with all debugging options enabled.
* `clean` - Clean up all build output files.

If `build.sh` isn't executable, fix the permissions with:
```bash
$ chmod u+x scripts/build.sh
```

Any extra options beyond the first will be passed directly to PyInstaller. See
[the manual](http://www.pyinstaller.org/export/develop/project/doc/Manual.html)
for more information, or do `pyinstaller --help` at the command line.

## Progress and notes

Please see the [wiki](https://github.com/chicken-mover/black-mango/wiki).
