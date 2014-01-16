#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source bashutils.sh

cd .git
if [ -d hooks ]; then
    mv hooks hooks-backup
fi
ln -s ../hooks hooks

