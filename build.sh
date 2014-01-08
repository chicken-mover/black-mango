#!/bin/bash

# cd to the directory of the build script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

PROG=pyinstaller

# This option is recommended under Windows, according to the PyInstaller docs.
if [ "$(expr substr $(uname -s) 1 6 2>&1)" == "CYGWIN" ]; then
    STRIP_SYMBOLS=''
else
    STRIP_SYMBOLS='--strip'
fi

ALL_OPTIONS=(
    --distpath=./dist/
    --workpath=./build/
    --log-level=INFO
    --specpath=./spec/
    --name=BlackMango
    --onefile
    --windowed
)

DEBUG_OPTIONS=(
    --debug
)

NODEBUG_OPTIONS=(
    --onefile
)

SCRIPTPATH=./blackmango/__init__.py

function make() {
    $PROG ${ALL_OPTIONS[@]} ${NODEBUG_OPTIONS[@]} $STRIP_SYMBOLS $SCRIPTPATH
}

function clean() {
    rm -rfv ./dist/
    rm -rfv ./build/
    rm -rfv ./spec/
    rm -vf *.spec
}

function make-debug() {
    $PROG ${ALL_OPTIONS[@]} ${DEBUG_OPTIONS[@]} $SCRIPTPATH
}

function help() {
    echo "Usage: $0 [make|clean|make-debug]"
}

case "$1" in
    make)
        make
        exit
        ;;
    clean)
        clean
        exit
        ;;
    make-debug)
        make-debug
        exit
        ;;
    make-clean)
        make-clean
        exit
        ;;
esac

help
exit 1