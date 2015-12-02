# Black Mango

Please make sure to add docstrings to everything and adhere to the
[style guide](https://github.com/chicken-mover/black-mango/wiki/Style-guide).

Git commit messages should follow 
[the standard format](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).

## Setup

### Set up Black Mango

To set up everything in a virtualenv, do:

```bash
$ mkvirtualenv black-mango
$ git clone https://github.com/chicken-mover/black-mango
$ cd black-mango
$ pip install -r requirements.txt
$ python setup.py develop
```

### Install PyInstaller (for creating distributable one-file packages)

```bash
$ git clone git://github.com/pyinstaller/pyinstaller.git
$ cd pyinstaller
$ sudo python setup.py install
```

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

### Running the development version

Once you have set up Black Mango, you can run the program with all debug flags
set by executing the script `run-debug.sh`:
```bash
$ ./scripts/run-debug.sh
```

To run the program manually, simply execute the `__init__.py` file and pass any
command line flags directly. To see a complete list of flags, do
```bash
$ python blackmango/__init__.py --help
```

## Build instructions

**Note that the build process is still being worked out, so the instructions
below should be considered highly experimental.**

After running the setup command above, you can run the `build.sh` script from
the project directory like so:
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
