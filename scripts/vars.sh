#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# If we are in a virtualenv, then it will be assumed that the version of Python
# is known to be correct.
if [ -z "$VIRTUALENV" ]; then
    # On Debian stable, 'python' is 2.7, but on Arch it is 3.x
    PYTHON="python"
    # Explicitly named Python 2.? is better
    if hash python2 >/dev/null 2>&1; then
        PYTHON=python2
    fi
    # An explicitly named Python 2.7 binary is better than a 2.? binary.
    if hash python2.7 >/dev/null 2>&1; then
        PYTHON=python2.7
    fi
    # If the Mac-specific Python 2.7 installer has been run, that takes priority.
    MAC_PYTHON27="/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7"
    if [ -f $MAC_PYTHON27 ]; then
        PYTHON=$MAC_PYTHON27
    fi
else
    PYTHON="python"
fi

PYINSTALLER=$(which pyinstaller)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
RESOURCE_PATH=$BASEDIR/assets

export BASEDIR
export BRANCH
export PYINSTALLER
export PYTHON
export RESOURCE_PATH
