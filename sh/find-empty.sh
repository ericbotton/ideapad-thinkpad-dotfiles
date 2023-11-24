#!/bin/bash

# This script finds all empty files in a directory recursively

# Check if the user provided a directory path
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Check if the provided directory path is valid
if [ ! -d "$1" ]; then
    echo "Error: $1 is not a valid directory"
    exit 1
fi

# Find all empty files in the directory recursively
find "$1" -type f -empty
