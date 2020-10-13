#!/bin/bash

DIRECTORY=$(dirname $0)
source "$DIRECTORY/venv/bin/activate"
directory=$1
inotifywait -m $directory -e create -e moved_to |
    while read dir action file; do
        python3 "$DIRECTORY"/main.py "$dir$file"
    done