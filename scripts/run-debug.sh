#!/bin/bash

# cd to the directory of the build script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

source scripts/vars.sh

$PYTHON blackmango/__init__.py \
    --debug=$($PYTHON -c "import logging;print logging.DEBUG") $@
