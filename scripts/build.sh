#!/bin/bash

# TODO: Turn this into a proper Makefile at some point.

# cd to the directory of the build script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source vars.sh

cd ../build
echo "Copying source tree..."
cp -rv ../blackmango ./

echo "Comiling submodules with Cython ..."
find . -type f -name '*.py' -exec cython -f {} \;
# TODO: Actual compile step. Probbaly do this part and the immediately preceding
# command with distutils: http://docs.cython.org/src/reference/compilation.html


# This option is not recommended under Windows, according to the PyInstaller
# docs.
if [ "$(expr substr $(uname -s) 1 6 2>&1)" == "CYGWIN" ]; then
    PYINSTALLER_STRIP_SYMBOLS=''
else
    PYINSTALLER_STRIP_SYMBOLS='--strip'
fi

PYINSTALLER_ALL_OPTIONS=(
    --distpath=./dist/
    --workpath=./build/
    --specpath=./spec/
    --log-level=INFO
    --name=BlackMango
    --one-dir
    --windowed
)

PYINSTALLER_DEBUG_OPTIONS=(
    --debug
)

PYINSTALLER_NODEBUG_OPTIONS=(
    $STRIP_SYMBOLS
)

PYINSTALLER_RESOURCES=()

function load-resources() {
    for resource in $(find $RESOURCE_PATH -type f); do
        r="--resource=$resource,DATA,$(basename $resource)"
        echo "Found resource $r"
        PYINSTALLER_RESOURCES+=($r)
    done
}

PYINSTALLER_SCRIPTPATH="blackmango/__init__.py"

function make() {
    load-resources
    $PYTHON -OO $PYINSTALLER ${PYINSTALLER_ALL_OPTIONS[@]} \
        ${PYINSTALLER_NODEBUG_OPTIONS[@]} ${PYINSTALLER_RESOURCES[@]} \
        $PYINSTALLER_SCRIPTPATH $@
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
    $PYINSTALLER ${PYINSTALLER_ALL_OPTIONS[@]} ${PYINSTALLER_DEBUG_OPTIONS[@]} \
         $PYINSTALLER_SCRIPTPATH ${PYINSTALLER_RESOURCES[@]} $@
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
