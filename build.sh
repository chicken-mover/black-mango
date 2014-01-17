#!/bin/bash

# TODO: Turn this into a proper Makefile at some point.

# cd to the directory of the build script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source scripts/vars.sh

# This option is not recommended under Windows, according to the PyInstaller
# docs.
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

RESOURCES=()

function load-resources() {
    for resource in $(find $RESOURCE_PATH -type f); do
        r="--resource=$resource,DATA,$(basename $resource)"
        echo "Found resource $r"
        RESOURCES+=($r)
    done
}

SCRIPTPATH="blackmango/__init__.py"

function make() {
    load-resources
    $PYTHON -OO $PYINSTALLER ${ALL_OPTIONS[@]} ${NODEBUG_OPTIONS[@]} ${RESOURCES[@]} \
        $SCRIPTPATH $@
}

function clean() {
    rm -rfv ./dist/
    rm -rfv ./build/
    rm -rfv ./spec/
    rm -vf *.spec
    for f in $(find . -type f -name '*.py[co]'); do
        echo "rm" $(rm -rv $f)
    done
}

function make-debug() {
    load-resources
    $PYINSTALLER ${ALL_OPTIONS[@]} ${DEBUG_OPTIONS[@]} $SCRIPTPATH ${RESOURCES[@]} $@
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
