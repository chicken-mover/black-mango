#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

source scripts/vars.sh

cd .git
if [ -d hooks ]; then
    mv hooks hooks-backup
elif [ -L hooks ]; then
    rm hooks
fi
ln -s ../scripts/hooks hooks
chmod u+x hooks/*

