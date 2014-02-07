#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source vars.sh

echo "Performing automatic push to origin/$BRANCH (CTL-C to abort)"
sleep 2 && git push origin $BRANCH && git push --tags