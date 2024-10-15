#!/bin/bash
 
if [ $# -ne 3 ]; then
    echo "Usage: $0 <source_directory> <destination_directory> <filename_list>"
    exit 1
fi
 
SOURCE_DIR=$1
DEST_DIR=$2
FILENAME_LIST=$3
 
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory $SOURCE_DIR does not exist."
    exit 1
fi
 
if [ ! -d "$DEST_DIR" ]; then
    mkdir -p "$DEST_DIR"
fi
 
if [ ! -f "$FILENAME_LIST" ]; then
    echo "File list $FILENAME_LIST does not exist."
    exit 1
fi
 
cat "$FILENAME_LIST" | tr -d '[:space:]' | tr -d ',' | xargs -P 8 -I {} bash -c 'if [ -f "$0/{}" ]; then cp "$0/{}" "$1"; echo "Copied {} to $1"; else echo "File {} not found in $0"; fi' "$SOURCE_DIR" "$DEST_DIR"
