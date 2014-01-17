#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

PYTHON="python"
if hash python2 >/dev/null 2>&1; then
    PYTHON=python2
fi
if hash python2.7 >/dev/null 2>&1; then
    PYTHON=python2.7
fi

MAC_PYTHON27="/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7"
if [ -f $MAC_PYTHON27 ]; then
    PYTHON=$MAC_PYTHON27
fi

PYINSTALLER=$(which pyinstaller)

BRANCH=$(git rev-parse --abbrev-ref HEAD)

RESOURCE_PATH=$BASEDIR/assets

export BASEDIR
export BRANCH
export PYINSTALLER
export PYTHON
export RESOURCE_PATH
