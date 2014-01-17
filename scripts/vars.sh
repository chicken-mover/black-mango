#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}"/.. )" && pwd )"

PYTHON="python"
if hash python2 >/dev/null 2>&1; then
    PYTHON=python2
fi
if hash python2.7 >/dev/null 2>&1; then
    PYTHON=python2.7
fi

PYINSTALLER=$(which pyinstaller)

BRANCH=$(git rev-parse --abbrev-ref HEAD)

RESOURCE_PATH=$BASEDIR/assets

export BASEDIR
export BRANCH
export PYINSTALLER
export PYTHON
export RESOURCE_PATH
