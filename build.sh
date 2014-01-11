#!/bin/sh

# cd to the directory of the build script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

PROG=$(which pyinstaller)

PYTHON="python"
if hash python2 >/dev/null 2>&1; then
    PYTHON=python2
fi
if hash python2.7 >/dev/null 2>&1; then
    PYTHON=python2.7
fi

# This option is recommended under Windows, according to the PyInstaller docs.
if [ "$(expr substr $(uname -s) 1 6 2>&1)" == "CYGWIN" ]; then
    STRIP_SYMBOLS=''
else
    STRIP_SYMBOLS='--strip'
fi

ALL_OPTIONS=(
    --distpath=./dist/
    --workpath=./build/
    --specpath=./spec/
    --log-level=INFO
    --name=BlackMango
    --onefile
    --windowed
)

DEBUG_OPTIONS=(
    --debug
)

NODEBUG_OPTIONS=(
    $STRIP_SYMBOLS
)

SCRIPTPATH="blackmango/__init__.py"

function make() {
    $PYTHON -OO $PROG ${ALL_OPTIONS[@]} ${NODEBUG_OPTIONS[@]} $SCRIPTPATH $@
}

function clean() {
    rm -rfv ./dist/
    rm -rfv ./build/
    rm -rfv ./spec/
    rm -vf *.spec
    for f in $(find . -type f | grep -E "\.py(c|o)$"); do
        rm -rv $f
    done
}

function make-debug() {
    $PROG ${ALL_OPTIONS[@]} ${DEBUG_OPTIONS[@]} $SCRIPTPATH $@
}

function help() {
    echo "Usage: $0 [make|clean|make-debug]"
}

function this-exit() {
    cd -
    exit $1
}

case "$1" in
    make)
        shift
        make $@
        this-exit
        ;;
    clean)
        clean
        exit
        ;;
    make-debug)
        shift
        make-debug $@
        this-exit
        ;;
esac

help
this-exit 1
